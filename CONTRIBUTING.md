# Contributing

Contributions are welcome when they make a benchmark easier to reproduce,
stronger to challenge, or more precise about its limitations.

## New project entry

A new entry must include:

- at least one official paper, tracker item, or source repository;
- a public implementation or a sufficiently detailed public project report;
- a real hardware result;
- a named classical baseline for the same task or observable;
- separate timing scopes for quantum and classical work;
- a short result summary;
- an explicit claim boundary.

Copy `ENTRY_TEMPLATE.json`, use a unique `id`, and keep numerical values in SI
seconds. Use `null` when a quantity is unavailable. Do not replace an unknown
value with zero.

## Classical challenge

A classical challenge is equally valuable. Include the algorithm, hardware,
software versions, precision target, convergence evidence, wall-time scope, and
an artifact or repository that others can inspect.

If the new result weakens an existing quantum classification, update the entry.
The purpose of this project is accurate comparison, not preserving a ranking.

## Validation

```bash
python scripts/build.py
python scripts/build.py --check
python -m unittest discover -s tests
```

Generated files under `docs/` must be committed with the source entry change.

