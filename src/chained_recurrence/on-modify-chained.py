#!/usr/bin/env python

import os
import sys
from datetime import datetime
from time import sleep

from tasklib import Task, TaskWarrior


class ChainedTask(Task):
    @classmethod
    def create_link(cls, origin_task):
        """
        Creates a subsequent task based on `origin_task`.
        """
        excluded = Task.read_only_fields + ['start', 'end']
        data = {
            key: origin_task._data[key]
            for key in origin_task._data if key not in excluded
        } | {'chainedPrev': origin_task.uuid}

        if (delta := origin_task.due_delta) is not None:
            data['due'] = datetime.now() + delta

        if (delta := origin_task.wait_delta) is not None:
            data['wait'] = datetime.now() + delta
            data['status'] = 'waiting'
        else:
            data['status'] = 'pending'

        task = cls(origin_task.backend, **data)
        task.save()

        origin_task._data['chainedNext'] = task.uuid
        origin_task.save()

        return task

    @property
    def is_chained(self):
        return self._data.get('chained', 'off') == 'on'

    @property
    def status_changed(self):
        return self._data['status'] != self._original_data['status']

    @property
    def due_delta(self):
        if 'due' in self._data:
            return abs(self._data['due'] - self._data['entry'])

    @property
    def wait_delta(self):
        if 'wait' in self._data:
            return abs(self._data['wait'] - self._data['entry'])

    @property
    def uuid(self):
        if 'uuid' in self._data:
            return self._data['uuid'].split('-', 1)[0]


def process_initial_task(tw):
    """
    Performs the initial modification.
    """
    task = ChainedTask.from_input(backend=tw)
    print(task.export_data(), flush=True)
    return task


def wait_taskwarrior():
    """
    Waits for Taskwarrior to exit, so we're free to modify `.data` files.
    """
    task_pid = os.getppid()

    if os.fork() != 0:
        sys.exit()

    os.close(1)

    while os.path.exists(f'/proc/{task_pid}'):
        sleep(0.1)


def main():
    tw = TaskWarrior()
    tw.overrides.update({'recurrence': 'no', 'hooks': 'no'})

    task = process_initial_task(tw)

    if task.status_changed and task.completed and task.is_chained:
        print('Creating new chained task.', flush=True)
        wait_taskwarrior()
        ChainedTask.create_link(task)


if __name__ == '__main__':
    main()
