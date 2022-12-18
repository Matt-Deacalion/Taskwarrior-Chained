# Taskwarrior Chained Recurrence Hook

Painlessly adds chained recurrence to Taskwarrior. Requires `Python >= 3.8`.

<img src="https://raw.githubusercontent.com/Matt-Deacalion/Taskwarrior-chained/trunk/illustration.svg" alt="recurring task illustration" width="800"/>

In the illustration above, task `26ccff69` is automatically created when task
`90e414dl` is completed. With the new task having equivalent `due` and `wait`
attributes, relative to it's own `entry` attribute.


## Install

```bash
$ pip install chained-recurrence
$ chained-recurrence install
```


## Usage

Create tasks as you usually would, adding `chained:on`:

```bash
$ task add chained:on 'hair cut'
```

When this task's status is changed to `complete`, a new one will be created.

The `wait` and `due` attributes can also be used, their date and time values
will be updated in relation to the current date and time:

```bash
# command run at 2023-01-01 18:00:00
$ task add chained:on wait:1d 'workout'

# command run at 2023-01-20 18:00:00, the new 'workout' task will have a `wait`
# value of: 2023-01-21 18:00:00
$ task 1 done
```

```bash
$ task add chained:on wait:1d due:5d 'workout'
```


## Uninstall

```bash
$ chained-recurrence uninstall
$ pip uninstall chained-recurrence
```
