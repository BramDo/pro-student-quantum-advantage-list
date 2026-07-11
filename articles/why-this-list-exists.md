# Why the Pro Student Quantum Advantage List Exists

The Quantum Advantage Tracker is the inspiration for this project. It provides
a valuable public record of circuit instances, result metadata, and review
discussions.

The Pro Student Quantum Advantage List adds a different layer: an end-to-end
implementation around the official source. Each entry connects the paper or
tracker item to circuit construction, hardware execution, mitigation, a
classical competitor, timing definitions, numerical artifacts, and an explicit
claim boundary.

"Pro Student" means an advanced student, hobbyist, independent researcher, or
small laboratory with a capable laptop or workstation and cloud access to
quantum hardware, but without a dedicated supercomputer cluster.

## Local practical advantage

A local practical advantage exists when the measured quantum workflow reaches a
useful answer faster than a named classical workflow for the same stated task on
the resources actually available to the project.

This definition is conditional. It does not say that every classical algorithm,
GPU cluster, or future implementation is slower. It requires the benchmark to
name its hardware, timing scope, accuracy target, convergence status, and
excluded overhead.

The list should change when a stronger classical result appears. A successful
challenge improves the benchmark rather than invalidating the purpose of the
project.

## The first three projects

### Fermi-Hubbard dynamics on 120 qubits

The official experiment studies a one-dimensional Fermi-Hubbard chain. The
student-scale implementation reconstructs the mapping, Fire Opal route,
hardware observables, MPS reference, and an observable-specific Majorana
competitor.

The local timing comparison is strong, but it is not universal. The MPS
reference did not establish full convergence, and a later four-H200 classical
study demonstrates why the strongest available classical method matters.

### Non-Abelian SU(2) hadron dynamics

The official work uses a Loop-String-Hadron encoding on a 60-site lattice with
120 active qubits. The implementation links the official circuits and data to a
Fire Opal hardware route, local circuit-MPS checks, and the published
tensor-network and Pauli-propagation baselines.

The result supports runtime separation and circuit or sector validation.
Hardware-only time is not cloud wall time, and the local observable
normalization is not silently treated as identical to the published hadron
scalar.

### Operator Loschmidt Echo on 80 qubits

This project extends a released tracker circuit family to a declared 80-qubit
Kingston subgraph. Sixteen mitigated circuits produced a finite-sample OLE ratio
of `0.74028847 +/- 0.01663657`.

The complete Fire Opal action took 328 seconds. A tracker-linked BP-TN run at
bond dimension 64 did not finish even the delta half within 901 seconds. That is
a local runtime lower bound, not a matched-accuracy proof: the classical route
did not converge and did not complete the full ratio.

## Admission criteria

- An official paper, tracker entry, or source repository.
- A complete implementation rather than an isolated result value.
- A real quantum-hardware run with backend and mitigation recorded.
- A classical competitor for the same stated task or observable.
- Explicit timing definitions and excluded overhead.
- Disclosed accuracy, convergence, finite-sample, and scaling limitations.

## What the list does not claim

A sufficiently optimized classical implementation on a supercomputer may beat
any local reference in this repository. A new contraction order, symmetry
reduction, observable-specific method, or GPU implementation can change the
ranking.

The strongest defensible statement today is that the listed projects show local
practical or time-to-answer separation under declared resources. They are open
engineering and scientific benchmarks, not final complexity-theoretic
demonstrations.

Canonical public page:
<https://edukaizen.nl/pro-student-quantum-advantage-list/>
