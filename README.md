# Pro Student Quantum Advantage List

An open, extensible evidence register of student-scale quantum projects,
including local time-to-answer reports, runtime bounds, execution-metric
comparisons and diagnostic results under explicitly declared resources.

This repository complements the
[Quantum Advantage Tracker](https://quantum-advantage-tracker.github.io/). A
tracker entry can preserve a circuit and a result. This list adds the complete
project path: official source, implementation, hardware execution, mitigation,
classical competitor, timing definition, uncertainty, and claim boundary.

Read the public Edukaizen version:
[Pro Student Quantum Advantage List](https://edukaizen.nl/pro-student-quantum-advantage-list/).

## Definition

A **local practical advantage** means that a measured quantum workflow reached
a useful answer faster than a named classical workflow for the same stated task
on the resources actually available to the project.

It is not proof that every classical algorithm, GPU cluster, supercomputer, or
future implementation is slower. A stronger classical result is a successful
challenge and should update the list.

Execution-metric and diagnostic entries are also included, with separate labels.
An execution-metric ratio compares explicitly different clock scopes; it does
not establish a validated time-to-answer or matched-accuracy advantage.

## Current entries

<!-- advantage-list:start -->
8 active project reports. Register version 1.3.9; evidence through 2026-09-27; synchronized 2026-10-17.

| Project | Scale | Primary quantum timing | Classification |
|---|---:|---:|---|
| [1D Fermi-Hubbard](entries/fermi-hubbard-120q.json) | 120 qubits / 60 sites | 33.148928 s | Local time-to-answer separation |
| [SU(2) hadron dynamics](entries/su2-hadron-120q.json) | 120 qubits / 60 sites | 1.425408 s | Paper-aligned local separation |
| [Operator Loschmidt Echo Q80](entries/operator-loschmidt-echo-q80.json) | 80 qubits | 328 s | Local runtime lower bound |
| [Random Graph Sampling](entries/random-graph-sampling-70q.json) | 70 qubits | 19 s | Diagnostic only |
| [Floquet-Ising 51q](entries/floquet-ising-51q.json) | 51 qubits | 41 s | Partial task-specific time-to-signal advantage of 8.93x; accuracy is not matched |
| [2D Hubbard Nighthawk](entries/fermi-hubbard-2d-nighthawk-72q.json) | 72 qubits / 36 sites | 7 s | Local execution-metric ratio; accuracy unvalidated |
| [Nighthawk RCS](entries/nighthawk-rcs-61q.json) | 61 qubits | 19 s | Local execution-metric ratio; process fidelity unvalidated |
| [XXZham](entries/xxzham-80q.json) | 80 qubits / 80 sites | 76 s | Local execution-metric ratio; convergence unfinished |
<!-- advantage-list:end -->

The Nighthawk project has [nine public articles](https://edukaizen.nl/2d-local-quantum-advantage/).
Its raw research repository remains private. The approximately 181 s provider
running-to-finished interval, failed TFLO holdouts and uncertified chi64 reference
are preserved in its entry; the 7 QPU s are not end-to-end time.

The PBMC68k QML entry was withdrawn after its local-advantage claim failed the
September 2026 audit. Its earlier version remains in Git history; it is absent
from the active entries, generated pages and feed.
The Nighthawk RCS marginal threshold is exploratory and was selected after the
measurements. A circuit-independent random generator can pass that low-order
check, but it does not simulate the circuit and is not an eligible process
competitor. The MPS timing comparison is therefore retained with an explicit
unvalidated process-fidelity boundary.

## Why student and hobbyist projects matter

Quantum advantage should not be only a headline produced by large laboratories.
Students, hobbyists, independent researchers, and small teams can publish useful
benchmarks when they state exactly what was compared and where the comparison
ends.

The goal is not to protect a quantum win. The goal is to create an open target.
If somebody finds a faster tensor-network contraction, uses symmetry more
effectively, runs a better GPU implementation, or shows that a local advantage
disappears, the benchmark has done its job.

Quantum programming also needs its **Visual Basic or C# moment**: easy to start,
possible to inspect, and capable of preserving the low-level evidence needed for
scientific review. Read the full essay:
[Quantum Advantage Needs a Visual Basic Moment](articles/quantum-advantage-needs-a-visual-basic-moment.md).

## Add or challenge an entry

1. Copy [`ENTRY_TEMPLATE.json`](ENTRY_TEMPLATE.json) into `entries/`.
2. Give the entry a stable lowercase ID and complete every required field.
3. Link an official paper, tracker entry, or source repository.
4. State the quantum and classical timing scopes separately.
5. Include accuracy, convergence, finite-sample, and scaling limitations.
6. Run `python scripts/build.py` and `python -m unittest discover -s tests`.
7. Open a pull request, or use one of the repository issue templates.

The eight JSON records in `entries/` are the authoritative source for the
generated register, Edukaizen page, README table and
[`docs/github-profile-projects.md`](docs/github-profile-projects.md).
Run `python scripts/build.py` after changing an entry. Publish
`docs/edukaizen-page.html` to the existing Edukaizen page and copy the generated
profile block into `BramDo/BramDo/README.md`; retain the block markers.
`python scripts/build.py --check` detects stale generated content.
The synchronization date records publication maintenance; the evidence date
continues to record the underlying experiment or analysis.

The machine-readable contract is documented in
[`schema/entry.schema.json`](schema/entry.schema.json). The generated public feed
is [`docs/data/advantage-list.json`](docs/data/advantage-list.json).

## Admission criteria

- An official paper, tracker entry, or source repository.
- A complete implementation rather than an isolated result value.
- A real quantum-hardware run with backend and mitigation recorded.
- A classical competitor aimed at the same stated observable or task.
- Explicit wall-time definitions and excluded overhead.
- Disclosed accuracy, convergence, finite-sample, and scaling limitations.

## Repository layout

- `entries/`: one machine-readable JSON file per project.
- `schema/`: the extensible entry contract.
- `articles/`: the non-technical story and publication text.
- `docs/`: generated GitHub Pages site and public JSON feed.
- `scripts/build.py`: validation and deterministic site/feed generator.
- `tests/`: structural and claim-boundary regression tests.

## Claim policy

This list does not certify formal complexity-theoretic quantum advantage. Its
strongest current category is local practical or time-to-answer separation under
declared resources. Labels must become weaker when convergence, matched accuracy,
or timing parity is missing.

## License

Code is released under the MIT License. Written content and entry metadata are
released under CC BY 4.0; attribution should name the repository and the linked
project authors.
