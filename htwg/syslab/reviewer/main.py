#!/usr/bin/env python3

from cmd import Cmd
from os.path import expanduser, join
from typing import Dict, Any

from github import Github
from ruamel import yaml


def read_config(file_path: str) -> Dict[str, Any]:
    # validate
    # c = Core(source_file=file_path, schema_files=[CONFIG_SCHEMA_FILEPATH])
    # c.validate(raise_exception=True)

    with open(file_path) as f:
        config = yaml.safe_load(f)

    return config


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


if __name__ == '__main__':
    config = read_config(join(expanduser('~'), '.syslab-reviewer.yml'))
    g = Github(config['github']['token'])

    user = g.get_user()
    print(user)

    org = g.get_organization('htwg-syslab-bsys')
    print(org)

    for repo in org.get_repos():
        print(repo)

        for pr in repo.get_pulls():
            print('\t', pr)

            for comment in pr.get_comments():
                print('\t\t', comment)

    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')
