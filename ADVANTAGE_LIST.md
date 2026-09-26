# Pro Student Quantum Advantage List

Generated from the validated files in `entries/`. The classification is
conditional on each entry's declared resources and claim boundary.

| Project | Scale | Primary quantum timing | Classification |
|---|---:|---:|---|
| [1D Fermi-Hubbard](entries/fermi-hubbard-120q.json) | 120 qubits / 60 sites | 33.148928 s | Local time-to-answer separation |
| [SU(2) hadron dynamics](entries/su2-hadron-120q.json) | 120 qubits / 60 sites | 1.425408 s | Paper-aligned local separation |
| [Operator Loschmidt Echo Q80](entries/operator-loschmidt-echo-q80.json) | 80 qubits | 328 s | Local runtime lower bound |
| [Random Graph Sampling](entries/random-graph-sampling-70q.json) | 70 qubits | 19 s | Diagnostic only |
| [Floquet-Ising 51q](entries/floquet-ising-51q.json) | 51 qubits | 41 s | Local time-to-answer separation |
| [2D Hubbard Nighthawk](entries/fermi-hubbard-2d-nighthawk-72q.json) | 72 qubits / 36 sites | 7 s | Local execution-metric ratio; accuracy unvalidated |
| [Nighthawk RCS](entries/nighthawk-rcs-61q.json) | 61 qubits | 19 s | Local execution-metric ratio; accuracy unvalidated |
| [XXZham](entries/xxzham-80q.json) | 80 qubits / 80 sites | 76 s | Local execution-metric ratio; accuracy unvalidated |

## Fermi-Hubbard dynamics on 120 qubits

A 60-site Fermi-Hubbard hardware workflow produced local charge, spin, and double-occupancy observables and was compared with local MPS and observable-specific Majorana calculations.

**Comparison:** The quantum execution proxy was 272.50x shorter than the local chi=256 MPS wall time for this declared instance.

**Quantum result:** The hardware produced a full 120-qubit observable profile; raw mean double occupancy was 0.22862549 and readout-corrected mean double occupancy was 0.23067722.

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

**Quantum result:** The local hardware route produced charge-sector and differential-observable data for the 120-qubit circuit family.

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

**Quantum result:** The measured delta/delta0 OLE ratio was 0.74028847 +/- 0.01663657; all eight sample ratios were positive.

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

## Random Graph Sampling on 70 data qubits

A complete 70-data-qubit non-Clifford circuit was sampled on IBM hardware, alongside an independent 70+8-qubit stabilizer-verification workflow and local classical scaling studies.

**Comparison:** Hardware returned 256 samples in 19 quantum-seconds, while a local Aer fit projects about 6.89 million years for one 70-qubit sample; sample counts and output quality are not matched.

**Quantum result:** The complete circuit returned 256 samples. The separate checked dataset retained 4,519 of 184,320 shots and gave a graph-state-prefix point estimate of 0.01217; its predeclared one-sided 95 percent lower-bound test failed. The original restricted-access IBM Boston execution reported substantially stronger effective performance than this independently accessible Kingston reproduction.

**Official sources**

- [Quantum Advantage Tracker issue 151](https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/issues/151)
- [Released Random Graph Sampling circuits](https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/tree/main/data/classically-verifiable-problems/circuit-models/random_graph_sampling)

**Implementation**

- [Edukaizen project](https://edukaizen.nl/random-graph-sampling/)
- [GitHub repository](https://github.com/BramDo/random_graph)

**Claim boundary**

- The Tracker result used restricted access to IBM Boston, whereas this independent reproduction used the available IBM Kingston route; backend access, physical mapping, and calibration window are therefore not matched.
- Boston produced a substantially stronger workload-level result, but its historical calibration and complete raw fidelity-analysis record are not public, so the result does not establish that Boston was universally better hardware than Kingston.
- The 70-qubit classical runtime is extrapolated from measurements ending at 12 qubits, not measured at full width.
- The quantum samples have no validated full-distribution fidelity, and the separate predeclared 95 percent stabilizer test failed.
- The post-hoc 75 percent lower bound is an exploratory sensitivity result, not 75 percent fidelity and not evidence of quantum advantage.

## Floquet-Ising oscillation detection on 51 qubits

A complete 51-qubit IBM Fez PEA/ZNE trajectory detected a reproducible Floquet-Ising oscillation in less declared execution time than a local D=64 PEPS simple-update trajectory for the same coordination-two magnetization.

**Comparison:** The 41-QPU-second PEA/ZNE route detected the 51-qubit oscillation 8.93x sooner than the 366.17-second local D=64 PEPS-SU trajectory under the declared timing scopes.

**Quantum result:** The fitted PEA/ZNE period was 4.76 cycles with profile interval 4.62 to 4.92; the fitted oscillation amplitude was about 5.2 conditional fit standard errors, consistent with two independent raw plus M3 trajectories at periods 4.48 and 4.61.

**Official sources**

- [Leviatan et al., Quantum Simulations beyond Classical Capabilities with Error-Mitigated Dynamic Circuits](https://arxiv.org/abs/2607.24937)
- [Quantum Advantage Tracker repository](https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io)

**Implementation**

- [Edukaizen project](https://edukaizen.nl/floquet-ising-toy-model/)
- [GitHub repository](https://github.com/BramDo/FLOQUET-QEM)

**Claim boundary**

- This is a partial, task-specific practical time-to-signal advantage, not a general or complexity-theoretic quantum-advantage claim.
- The 41-second timing is QPU execution only and excludes queueing, orchestration, retrieval, analysis, and classical mitigation processing.
- The classical D=64 PEPS-SU trajectory is converged by the declared low-D diagnostic only through cycle 8; cycles 9-16 are not a claim-ready classical reference.
- Across the eight trusted cycles, PEA/ZNE has diagnostic SRMSE 3.154 and maximum absolute z-score 6.932, so the preregistered matched-accuracy thresholds are not met.
- The local PEPS-SU implementation is not the paper's PEPS-BP production method at D=512 and D=700, and a stronger observable-specific classical result may change the ranking.

## 2D Local Quantum Advantage: 6x6 Hubbard on Nighthawk

A student/hobby project ran full-fermion 6x6 Hubbard circuits on 72 modes and measured charge, spin and doublons. Its local milestone is circa 20x less registered QPU usage than the current laptop-side chi64 MPS kernel time. The timing ratio is measured; numerical accuracy and end-to-end advantage remain unvalidated.

**Comparison:** The local chi64 kernel took 150.819180 s versus 7 registered QPU s for the complete paired job: 21.55x, or circa 20x. The separate 8-QPU-second job gives 18.85x. This is an execution-metric ratio, not an end-to-end or matched-accuracy speedup.

**Quantum result:** Readout+TFLO original gave N=31.39633 and D/site=0.090130; compact gave N=31.23064 and D/site=0.077194. Sitewise charge/spin/doublon RMS differences from the uncertified chi64 reference were 0.083889/0.091851/0.050805 (original) and 0.109304/0.125864/0.064116 (compact). Both TFLO holdout checks failed; reconstructed local probabilities reached -0.077303 and -0.092726. These target estimates are unvalidated.

**Official sources**

- [Project authors' Nighthawk source and archived runs (private; permission required)](https://github.com/BramDo/fermi-hubbard-2d-nighthawk)

**Implementation**

- [Edukaizen project](https://edukaizen.nl/2d-local-quantum-advantage/)
- [GitHub repository](https://github.com/BramDo/fermi-hubbard-2d-nighthawk)

Nine detailed Edukaizen articles and this register entry are public. The complete source, raw runs and theory archive remain in a private GitHub repository; access requires permission. Admission uses the public project-report route, not a claim that the complete implementation is publicly downloadable.

**Claim boundary**

- The approximately 20x milestone compares local classical kernel time with registered QPU usage. It is not a 20x shorter end-to-end run or a matched-accuracy quantum advantage.
- The 7 seconds cover the entire paired job, not each arm. The earlier 8-second DD/TFLO result is a separate job; mitigation settings and budgets must not be mixed.
- The latest provider running-to-finished interval was about 181 seconds, already longer than the 150.819-second classical kernel; queueing, preparation and local analysis add other overheads.
- The chi64 reference has no certified 6x6 error bound and is not converged. Chi128 was not performed, and its estimated cost cannot be counted as extra measured quantum speedup. Concurrent local work also limits timing comparability.
- Both TFLO holdout checks failed and some reconstructed probabilities are negative. The reported charge, spin and doublon estimates remain unvalidated; apparent agreement of individual observables does not validate the estimator.
- Exact N=32 is a model constraint, not a replacement for measured N. Original and compact results retain their own measured values and reference differences.
- This local resource comparison does not establish superiority to all classical algorithms, Google/Bonsai results, or a superconducting-material simulation. The 72-mode model and two-step finite circuit define the tested task.
- The public reports describe the evidence, but the raw research archive remains private. Full independent reproduction therefore requires access permission; listing the project does not remove this limitation.

## Nighthawk random-circuit sampling on 61 qubits

The released 61-qubit depth-36 circuit returned one million bitstrings on IBM Phoenix in 19 registered QPU seconds. A local chi=128 MPS simulation of the same logical circuit took 1,248.95 seconds for 1,000 bitstrings, a 65.7x execution-metric contrast. Its one-bit RMS discrepancy was 0.09047, within an exploratory 0.10 hobby tolerance; process-level fidelity was not independently matched.

**Comparison:** The 19-second QPU usage was 65.7x shorter than a 1,248.95-second local chi=128 MPS simulation of the same released circuit. The MPS one-bit RMS discrepancy of 0.09047 passes an exploratory 0.10 hobby tolerance, but circuit-level fidelity was not matched.

**Quantum result:** The IBM job returned one million 61-bit strings and repeated the released circuit's scale and shot count. This project did not independently calculate full-width ideal-probability XEB or fidelity for those strings.

**Official sources**

- [Original 61-qubit Nighthawk preprint](https://arxiv.org/abs/2609.28657)
- [Paper-linked circuit and analysis repository](https://github.com/BlueQubitDev/rcs-nighthawk)

**Implementation**

- [Edukaizen project](https://edukaizen.nl/nighthawk-61-qubit-random-circuit-sampling-en/)
- [GitHub repository](https://github.com/BramDo/rcs-nighthawk-replication)

The public repository contains code and article sources. The raw million-shot research data and large binaries were not included in that public release.

**Claim boundary**

- The 0.10 RMS band is an exploratory post-measurement hobby criterion on one-bit probabilities, much looser than the approximately 0.018 noise-only 95% threshold for 1000 shots.
- A circuit-independent random-bit generator also passes the one-bit RMS check; it is only a negative control for the check and is not a competitor for simulating the specified quantum process.
- The 19-second quantum value is QPU usage and the 1,248.95-second classical value is local simulator wall time; shot counts differ by a factor of 1000 and queue, preparation and analysis are excluded.
- Passing the coarse marginal band does not validate the full 61-bit distribution, ideal-circuit fidelity or full-width XEB. No independent full-distribution quality match was measured.
- The 65.7x number is a timing lead over one named circuit-following capped-MPS workflow. Without a matched process-fidelity estimate, it is not a demonstrated matched-quality, best-classical, full-distribution or end-to-end quantum advantage.

## XXZham: imbalance dynamics of 80 spins

IBM Kingston returned a complete 31-point imbalance curve for an 80-spin XXZ chain in 76 registered QPU seconds. Local TEBD took 130.69 seconds at chi=64, 1,503.99 seconds at chi=128 and 4,571.54 seconds at chi=256. The chi=128 to 256 refinement passes the 0.005 RMS stability limit but still misses the 0.01 maximum-change limit, so the QPU timing lead over these named settings remains descriptive rather than a matched-quality advantage.

**Comparison:** Registered QPU usage was 76 s: 1.72x shorter than local chi=64 TEBD at 130.69 s, 19.79x shorter than chi=128 at 1,503.99 s and 60.15x shorter than chi=256 at 4,571.54 s. Chi=256 improves the curve and passes the RMS refinement limit, but misses the maximum-change limit. This is an execution-time lead rather than a matched-quality quantum advantage.

**Quantum result:** The completed 80-spin run returned all 31 time points with RMSE 0.036943 against the tensor-network mean. A later 40-second-capped quantum attempt failed and yielded no complete curve.

**Official sources**

- [Quantum Advantage Tracker issue 244](https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/issues/244)
- [Original XXZ implementation](https://github.com/ak2y/Imbalance_XXZ_hz_1D)

**Implementation**

- [Edukaizen project](https://edukaizen.nl/xxzham-80-spins-nisq-quantum-computer/)
- [GitHub repository](https://github.com/BramDo/XXZham)

The Edukaizen series is public. The complete project repository is private; full independent reproduction requires access permission.

**Claim boundary**

- The five 8.012-second-median TEBD runs truly computed all 31 times to t=5, but chi=16 saturated early and its curve failed the required refinement stability. Its speed is not an accepted process-quality counterexample.
- The refined 130.69-second chi=64, dt=1/24 TEBD run was more accurate against the source curves but also failed convergence stability. It cannot be used as a qualified classical denominator for a quantum speedup.
- A new chi=128, dt=1/24 run completed in 1,503.99 seconds. Its source-mean RMSE improved from 0.009512 at chi=64 to 0.006382, but the chi=64 to 128 change was 0.007689 RMS and 0.021576 maximum, still beyond the selected 0.005 and 0.01 stability limits; time-step convergence at chi=128 was not tested.
- A chi=256, dt=1/24 run completed in 4,571.54 seconds with 31 finite points through t=5. The chi=128 to 256 curve change was 0.004477 RMS, inside the 0.005 limit, but its 0.013485 maximum still exceeded 0.01. The source-mean RMSE improved to 0.005135; time-step convergence at chi=256 was not tested.
- The reported 5.63x QPU/H200 ratio is a separate upstream Heron R3 comparison and is not a measured local laptop ratio.
- The later capped quantum trial failed, so no complete quantum result met the frozen local time-to-answer protocol.
- Registered QPU usage excludes queue, service overhead and local analysis. No matched-quality or full end-to-end local advantage comparison was established.
