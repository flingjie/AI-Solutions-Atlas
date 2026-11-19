# Write scope

`python3 scripts/validate.py` discovers problems across the whole repository.
It is a read-only check used to learn scope, not a command to fix the whole
repository.

A skill must only write:

- the record the caller named, or
- the file the current task asked it to create.

When validation reports errors outside that scope, report their path and
reason to the caller. Do not fix them.
