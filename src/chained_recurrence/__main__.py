#!/usr/bin/env python

import argparse
import os
import stat
import subprocess
import sys
from pathlib import Path
from subprocess import PIPE, Popen

import click
from tasklib import TaskWarrior

from . import __version__


class Installer:
    def __init__(self):
        self.udas = [
            ('uda.chained.type', 'string'),
            ('uda.chained.label', 'Chained Recurrence'),
            ('uda.chained.values', 'on,off'),
            ('uda.chained.default', 'off'),
            ('uda.chainedNext.type', 'string'),
            ('uda.chainedNext.label', 'Chained Next Link'),
            ('uda.chainedPrev.type', 'string'),
            ('uda.chainedPrev.label', 'Chained Previous Link'),
        ]

        tw = TaskWarrior()

        hook_name = 'on-modify-chained.py'
        self.hook_target = Path(__file__).resolve().parent / hook_name

        try:
            self.hook_link = Path(tw.config['hooks.location']) / hook_name
        except KeyError:
            self.hook_link = Path(tw.config['data.location']) / 'hooks' / hook_name

    def install(self):
        if self.hook_link.is_symlink():
            if self.hook_link.readlink() == self.hook_target:
                click.secho('Already installed: ', fg='green', nl=False)
                click.secho(click.format_filename(self.hook_link), fg='red')
                sys.exit()
            else:
                click.secho('Overwrite existing hook? [y/N]: ', fg='green', nl=False)
                answer = click.getchar().lower()
                click.echo()

                if answer != 'y':
                    print('aborted')
                    sys.exit()
                else:
                    self.hook_link.unlink(missing_ok=True)

        self.hook_link.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(self.hook_target, self.hook_link)
        self.hook_target.chmod(self.hook_target.stat().st_mode | stat.S_IEXEC)

        for uda in self.udas:
            cmd = Popen(['task', 'config', *list(uda)], stdin=PIPE, stdout=PIPE)
            cmd.communicate(b'YES\n')

        click.secho('Successfully installed!', bold=True, fg='green')

    def uninstall(self):
        try:
            self.hook_link.unlink()
        except FileNotFoundError:
            click.secho('Hook not found.', fg='red')
            sys.exit()

        for uda in self.udas:
            cmd = Popen(['task', 'config', uda[0]], stdin=PIPE, stdout=PIPE)
            cmd.communicate(b'YES\n')

        click.secho('Successfully uninstalled!', bold=True, fg='red')


def main():
    parser = argparse.ArgumentParser(
        prog='chained-recurrence',
        description='Painless chained recurrence for Taskwarrior.',
    )

    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        'action',
        help='add or remove hook, and update taskrc',
        choices=('uninstall', 'install'),
    )
    args = parser.parse_args()

    installer = Installer()

    if args.action == 'install':
        installer.install()
    else:
        installer.uninstall()


if __name__ == '__main__':
    main()
