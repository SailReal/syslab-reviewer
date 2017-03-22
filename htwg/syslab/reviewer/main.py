#!/usr/bin/env python3

from cmd import Cmd
from os.path import expanduser, join
from textwrap import indent
from typing import Dict, Any

from blessings import Terminal
from github import Github
from ruamel import yaml
import re


def read_config(file_path: str) -> Dict[str, Any]:
    # validate
    # c = Core(source_file=file_path, schema_files=[CONFIG_SCHEMA_FILEPATH])
    # c.validate(raise_exception=True)

    with open(file_path) as f:
        config = yaml.safe_load(f)

    return config


def iprint(text, depth=1, prefix=' '*4):
    print(indent(text, prefix*depth))


class MyPrompt(Cmd):

    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print('Hello, %s' % name)

    def do_quit(self, args):
        """Quits the program."""
        print('Quitting.')
        raise SystemExit


def github(t):
    config = read_config(join(expanduser('~'), '.syslab-reviewer.yml'))
    g = Github(config['github']['token'])

    user = g.get_user()
    print(user)
    print('You are logged in as: {} ({})'.format(user.name, t.bold(user.login)))

    courses = config['courses']
    print('courses:\n', ' '.join(courses.keys()))

    for course_name, course in courses.items():
        print('Course: {} ({})'.format(course_name, course['name']))
        github_course(course, g, t)


def github_course(course, g, t):
    repo_pattern = re.compile(course['repo_regex'])
    # repo_hw_pattern = re.compile(course['repo_homework'])

    org = g.get_organization(course['organization'])
    print(org)

    repos = {}

    for repo in org.get_repos():
        if not repo_pattern.fullmatch(repo.name):
            continue

        # add repo
        print(repo.name)
        repos[repo.name] = repo
        repo.pull_requests = {}
        # repos[repo.name]['pull_requests'] = {}

        for pr in repo.get_pulls(sort='created', direction='asc'):  # state='closed'
            # add pr
            repo.pull_requests[pr.number] = pr
            # repos[repo.name]['pull_requests'][pr.number] = pr

    # sort by creation of first (open) pull request
    repos_with_pr = [repo for repo in repos.values() if len(repo.pull_requests) > 0]
    for repo in sorted(repos_with_pr, key=lambda k: list(k.pull_requests.values())[0].created_at):
        # print(repo)
        depth = 1

        print('\n{}: (forks: {}, last push: {})'.format(repo.name, repo.forks_count, repo.pushed_at))
        iprint('ssh: {}'.format(repo.ssh_url), depth)

        for pr in repo.pull_requests.values():
            # print('\t', pr)
            # pr_issue = repo.get_issue(pr.number)

            depth = 1
            iprint('pr {}: {} (created: {}, updated: {}, assignees: {})'.format(t.bold(str(pr.number)), pr.title, pr.created_at,pr.updated_at, ', '.join([t.bold(assignee.login) for assignee in pr.assignees])), depth)
            depth = 2
            iprint('{}'.format(pr.html_url), depth)
            iprint('state: {}, merge status: {}'.format(t.bold(pr.state), pr.mergeable_state), depth)
            iprint('+ {}, - {} ({} files changed)'.format(pr.additions, pr.deletions, pr.changed_files), depth)

            # set assignee
            # pr_issue.edit(assignee=user)

            # # details
            # iprint('{}'.format(pr.body), depth)
            #
            # # pr_issue.get_comments()
            #
            # for comment in pr.get_comments():
            #     # iprint(comment, depth)
            #     depth += 1
            #     iprint('{}'.format(comment.path))
            #     iprint('{}'.format(comment.diff_hunk))
            #     depth += 1
            #     iprint('{}: {}'.format(t.bold(comment.user.login), comment.body), depth)
            #     iprint('')


def main():
    term = Terminal()

    # with term.fullscreen():
    #     github(term)

    github(term)

    # prompt = MyPrompt()
    # prompt.prompt = '> '
    # prompt.cmdloop('Starting prompt...')

if __name__ == '__main__':
    main()
