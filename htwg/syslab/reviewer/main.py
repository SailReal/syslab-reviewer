#!/usr/bin/env python3

import re
import warnings

from os.path import expanduser, dirname
from pathlib import Path
from textwrap import indent
from typing import Dict, Any

from colorama import init, Style
from github import Github
from pykwalify.core import Core
from ruamel import yaml

BOLD = Style.BRIGHT
RESET = Style.RESET_ALL

CONFIG_SCHEMA_FILEPATH = Path(dirname(__file__)) / '..' / '..' / '..' / 'config' / 'syslab-reviewer.schema.yml'

# ignore ruamel warning
warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)


def read_config(file_path: Path) -> Dict[str, Any]:
    # validate
    c = Core(source_file=str(file_path), schema_files=[str(CONFIG_SCHEMA_FILEPATH)])
    c.validate(raise_exception=True)

    with open(file_path) as f:
        config = yaml.safe_load(f)

    return config


def iprint(text, depth=1, prefix=' ' * 4):
    print(indent(text, prefix * depth))


def github():
    config = read_config(Path(expanduser('~')) / '.syslab-reviewer.yml')
    g = Github(config['github']['token'])

    user = g.get_user()
    print(user)
    print('You are logged in as: {} ({})'.format(user.name, BOLD + user.login + RESET))

    courses = config['courses']
    print('courses:\n', ', '.join([course['name'] for course in courses]))

    for course in courses:
        print('Course: {}'.format(course['name']))
        github_course(course, g)


def github_course(course: Dict[str, Any], g: Github):
    repo_pattern = re.compile(course['repo_regex'])

    org = g.get_organization(course['organization'])
    print(org)

    repos = {}

    for repo in org.get_repos():
        if not repo_pattern.fullmatch(repo.name):
            continue

        # add repo
        print(repo.name)
        repos[repo.name] = repo
        repo.issues = {}

        for issue in repo.get_issues(sort='created', direction='asc'):  # state='closed'
            # add issue
            repo.issues[issue.number] = issue

    # sort by creation of first (open) issue
    repos_with_issue = [repo for repo in repos.values() if len(repo.issues) > 0]
    for repo in sorted(repos_with_issue, key=lambda k: list(k.issues.values())[0].created_at):
        print('\n{}: (forks: {}, last push: {})'.format(repo.name, repo.forks_count, repo.pushed_at))

        for issue in repo.issues.values():
            depth = 1

            if issue.pull_request:
                pr = repo.get_pull(issue.number)
            else:
                pr = None

            issue_type = 'pr' if pr else 'issue'
            issue_template = '{issue_type} {number}: {title}' \
                             ' (created: {created_at}, labels: [{labels}], assignees: [{assignees}])'
            iprint(issue_template.format(
                issue_type=issue_type, number=BOLD + str(issue.number) + RESET,
                title=issue.title, created_at=issue.created_at,
                labels=', '.join([BOLD + label.name + RESET for label in issue.labels]),
                assignees=', '.join([BOLD + assignee.login + RESET for assignee in issue.assignees])), depth)

            depth = 2
            iprint('{}'.format(issue.html_url), depth)

            if pr:
                iprint('state: {}, merge status: {}'.format(BOLD + pr.state + RESET, pr.mergeable_state), depth)
                iprint('+ {}, - {} ({} files changed)'.format(pr.additions, pr.deletions, pr.changed_files), depth)

            # # details
            # iprint('{}'.format(issue.body), depth)
            #
            # # issue.get_comments()
            #
            # for comment in issue.get_comments():
            #     # iprint(comment, depth)
            #     depth += 1
            #     iprint('{}'.format(comment.path))
            #     iprint('{}'.format(comment.diff_hunk))
            #     depth += 1
            #     iprint('{}: {}'.format(BOLD + comment.user.login + RESET, comment.body), depth)
            #     iprint('')


def main():
    init()
    github()


if __name__ == '__main__':
    main()
