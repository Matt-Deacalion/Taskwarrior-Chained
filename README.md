# Taskwarrior Chained Recurrence Hook

Painlessly adds chained recurrence to Taskwarrior. Requires `Python >= 3.8`.

<img src="https://raw.githubusercontent.com/Matt-Deacalion/Taskwarrior-Chained/trunk/illustration.svg" alt="recurring task illustration" width="800"/>

In the illustration above, task `26ccff69` is automatically created when task
`90e414dl` is completed. With the new task having equivalent `due` and `wait`
attributes, relative to it's own `entry` attribute.

It's common to have `due` or `wait` fall on a *day boundary* such as `23:59` or
`00:00`, this is usually because a named date such as `eod` or `sod` was used
when creating the original task. If this is the case, new tasks will be created
with the `due` and `wait` attributes automatically falling on the equivalent
day boundaries.

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
$ task add chained:on wait:1d 'workout'
# previous command run at 2023-01-01T18:00:00

$ task 1 done
# previous command run at 2023-01-20T18:00:00, the new task has the following:
#   - wait: 2023-01-21T18:00:00
```

Compatibility with `named dates`:

```bash
$ task add chained:on wait:sod+1d due:eod+2d 'workout'
# previous command run at 2023-01-01T18:00:00

$ task 1 done
# previous command run at 2023-01-20T18:00:00, the new task has the following:
#   - wait: 2023-01-21T00:00:00
#   - due:  2023-01-22T23:59:59
```


## Uninstall

```bash
$ chained-recurrence uninstall
$ pip uninstall chained-recurrence
```
