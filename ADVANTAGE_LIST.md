# Pro Student Quantum Advantage List

Generated from the validated files in `entries/`. The classification is
conditional on each entry's declared resources and claim boundary.

| Project | Scale | Primary quantum timing | Classification |
|---|---:|---:|---|
| [1D Fermi-Hubbard](entries/fermi-hubbard-120q.json) | 120 qubits / 60 sites | 33.148928 s | Local time-to-answer separation |
| [SU(2) hadron dynamics](entries/su2-hadron-120q.json) | 120 qubits / 60 sites | 1.425408 s | Paper-aligned local separation |
| [Operator Loschmidt Echo Q80](entries/operator-loschmidt-echo-q80.json) | 80 qubits | 328 s | Local runtime lower bound |

## Fermi-Hubbard dynamics on 120 qubits

A 60-site Fermi-Hubbard hardware workflow produced local charge, spin, and double-occupancy observables and was compared with local MPS and observable-specific Majorana calculations.

**Comparison:** The quantum execution proxy was 272.50x shorter than the local chi=256 MPS wall time for this declared instance.

**Official sources**

- [Hartnett et al., large-scale Fermi-Hubbard digital quantum simulation](https://arxiv.org/abs/2605.04025)
- [Rausch et al., GPU and symmetry-aware classical challenge](https://arxiv.org/abs/2606.04771)

**Implementation**

- [Edukaizen project](https://edukaizen.nl/fermi-hubbard-quantum-simulation-project/)
- [GitHub repository](https://github.com/BramDo/fermi-hubbard-60q-tdvp)

**Claim boundary**

- This is a local time-to-answer result, not a reproduction of the paper's headline practical-advantage claim.
- The chi=256 MPS baseline did not establish full convergence.
- The fast Majorana route demonstrates that observable-specific classical methods can change the ranking.

## Non-Abelian SU(2) hadron dynamics on 120 active qubits

A Loop-String-Hadron implementation follows a differential hadron signal on a 60-site lattice and compares the quantum route with local circuit-MPS checks and published tensor-network and Pauli-propagation baselines.

**Comparison:** Both the local circuit checks and the paper-native baselines show a substantial runtime separation under their declared timing definitions.

**Official sources**

- [Ilcic et al., Observation of Robust and Coherent Non-Abelian Hadron Dynamics on Noisy Quantum Processors](https://arxiv.org/abs/2602.18080)
- [Quantum Advantage Tracker issue 149](https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/issues/149)
- [Official LSH-IBM circuit repository](https://github.com/indrakshir/LSH-IBM)
- [Official lsh_data repository](https://github.com/mathew0036/lsh_data)

**Implementation**

- [Edukaizen project](https://edukaizen.nl/hadron-quantumsimulatie/)
- [GitHub repository](https://github.com/BramDo/hadron)

**Claim boundary**

- Hardware-only time is not cloud wall time and excludes several service overheads.
- The local scalar normalization remains distinct from the tracker's published hadron scalar.
- The result supports runtime separation and circuit or sector validation, not an independent precision reproduction of every published observable.

## Operator Loschmidt Echo on 80 qubits

A tracker-compatible 80-qubit extension estimates an Operator Loschmidt Echo from finite computational-basis samples and compares the complete mitigated hardware action with a bounded tracker-linked BP-TN calculation.

**Comparison:** The incomplete bond-dimension-64 classical delta half alone exceeded the complete Fire Opal action by more than 2.75x on this machine.

**Official sources**

- [Quantum Advantage Tracker observable-estimation register](https://quantum-advantage-tracker.github.io/trackers/observable-estimations)
- [Released Operator Loschmidt Echo circuits](https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/tree/main/data/observable-estimations/circuit-models/operator_loschmidt_echo)

**Implementation**

- [Edukaizen project](https://edukaizen.nl/quantum-tracker-ole-q80-project/)
- [GitHub repository](https://github.com/BramDo/onderzoek_blackhole_echo_status_2026-03-05_131816)

**Claim boundary**

- The classical calculation did not converge and no matched-accuracy ratio was obtained.
- This is a tracker-compatible 80-qubit extension with N_init=8, not an official tracker instance or an N_init=500 reproduction.
- The observation is local and does not cover every classical implementation or optimized compute platform.
