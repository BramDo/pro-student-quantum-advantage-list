# Pro Student Quantum Advantage List

An open, extensible register of complete student-scale quantum projects that
show a **local practical quantum advantage** or **time-to-answer separation**
under explicitly declared resources.

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

## Current entries

| Project | Scale | Quantum timing used | Classical reference | Classification |
|---|---:|---:|---|---|
| [1D Fermi-Hubbard dynamics](entries/fermi-hubbard-120q.json) | 120 qubits / 60 sites | 33.148928 s execution proxy | 9,033 s local chi=256 MPS, plus Majorana checks | Local time-to-answer separation |
| [Non-Abelian SU(2) hadron dynamics](entries/su2-hadron-120q.json) | 120 active qubits / 60 sites | 1.425408 s hardware plus readout circuits | Local circuit MPS and published TN/Pauli-propagation baselines | Local and paper-aligned runtime separation |
| [Operator Loschmidt Echo Q80](entries/operator-loschmidt-echo-q80.json) | 80 qubits | 328 s complete Fire Opal action | BD=64 BP-TN delta half timed out after 901 s | Local lower bound greater than 2.75x; classical result not converged |

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

