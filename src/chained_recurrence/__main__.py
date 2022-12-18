#!/usr/bin/env python

import argparse
import os
import subprocess
from pathlib import Path
from subprocess import PIPE, Popen

from tasklib import TaskWarrior

from . import __version__

udas = [
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
hook_target = Path(__file__).resolve().parent / hook_name
hook_link = Path(tw.config['data.location']) / 'hooks' / hook_name


def install():
    os.symlink(hook_target, hook_link)

    for uda in udas:
        cmd = Popen(['task', 'config', *list(uda)], stdin=PIPE, stdout=PIPE)
        cmd.communicate(b'YES\n')


def uninstall():
    hook_link.unlink()

    for uda in udas:
        cmd = Popen(['task', 'config', uda[0]], stdin=PIPE, stdout=PIPE)
        cmd.communicate(b'YES\n')


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

    if args.action == 'install':
        install()
    else:
        uninstall()


if __name__ == '__main__':
    main()
