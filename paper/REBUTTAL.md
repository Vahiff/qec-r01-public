# Response to the Reported Gemini Review

**Manuscript:** *Finite-Calibration Bounds for Correlated-Noise Decoders in a 3-Qubit Repetition Code*  
**Project:** QEC-R01  
**Response status:** **Provisional author response to owner-summarized themes**, not a point-by-point response to an authenticated full review.  
**Source record:** [`REVIEW_GEMINI.md`](REVIEW_GEMINI.md). The full reviewer text was not supplied; statements below are **paraphrased themes**, not purported quotations.  
**Disposition:** The owner reports a **Reject** recommendation. We acknowledge that recommendation without representing this as formal journal peer review or an institutional assessment by Google.

We thank the reviewer for scrutinizing the scientific scope, execution evidence, and statistical interpretation. A rejection recommendation is a reason to improve the manuscript and identify unresolved validation requirements; it is not a reason to suppress inconvenient experimental limitations.

## Comment 1 — Scientific scope: three-qubit code, idealized noise, and no hardware results

**Response — Agree.** The three-qubit repetition code studied here addresses an X-only code-capacity model with perfect syndrome readout, one round, fixed independent flip probability, and one assumed paired-X correlation. It is not a fault-tolerant hardware experiment and is not a code capable of correcting arbitrary single-qubit Pauli faults. We acknowledged these constraints in the original manuscript's *Limitations and Discussion* section. They are material limitations of generalizability. Explicit disclosure does **not**, by itself, establish scientific novelty or make the scope sufficient for a research venue.

**Revision:** We now use the phrase *"This is a pilot code-capacity study"* in the abstract and add an explicit statement that the model is not a fault-tolerant hardware demonstration. We make no claims of device-level fault tolerance or simultaneous arbitrary X/Z-error correction.

## Comment 2 — QuTiP execution and DNS/package installation

**Response — Partly agree and clarify.** The reviewer is correct that the proposed QuTiP density-matrix/amplitude-damping validation has not executed, so the manuscript cannot claim to demonstrate agreement with it. The observed failed installation/import is an **environmental execution blocker**, not evidence that the numerical code passed or that the QuTiP experiment itself was scientifically validated. A dependency installation failure does not prove correctness of the model or software.

Nevertheless, recording the actual DNS failure, return codes, and missing dependency is an obligation of reproducible research, not a scientific impropriety. Fabricating successful installation output, physical simulation traces, or quantum-device results would be unacceptable. Our report expressly labels the QuTiP experiment **BLOCKED / NOT RUN** and excludes it from the quantitative QEC conclusions.

**Revision:** The manuscript retains this limitation. Independent QuTiP execution on an accessible, fully specified environment remains an outstanding validation task; it is not represented as completed.

## Comment 3 — Calibration replicates (R = 2,000) and reliability of results

**Response — Clarify the statistical estimand and limits.** We do **not** claim that 2,000 replicates are universally sufficient for quantum-error-correction research or for resolving rare logical-failure probabilities. In the specified idealized model, the decoder branch is determined by a binomial count: for each calibration shot, \(K\sim\mathrm{Binomial}(N,q_0)\), where \(q_0=p+(1-2p)b\). At the registered \(p=0.02\) and \(b=0.04\), \(q_0=0.0584\); MAP selects the paired-X branch when \(K/N>q_*=0.038816\). The finite-\(N\) branch-selection probability is therefore an **exact, model-conditional binomial tail**, calculable without Monte Carlo.

The R = 2,000 independent calibration repetitions estimate how often this decision is made by the implemented pseudorandom sampler. At \(N=1000\), 1,995/2,000 repetitions select the oracle branch (99.75%; Wilson 95% interval approximately 99.416%--99.893%). This precision suffices to show that the *observed* selection proportion exceeds the preregistered 95% criterion within the fixed model; it does **not** quantify model misspecification, calibration drift, hardware uncertainties, or independent scientific replicability. Logical failure rates in the reported table are exact enumerations over eight error masks **conditional on each selected decoder**, then averaged over calibrations; they are not empirical counts of device-level logical failures.

**Revision:** We explicitly separate (i) analytic probabilities under the idealized noise model, (ii) Monte Carlo calibration frequencies and confidence intervals, and (iii) validations still needed beyond this model. A larger study, broader noise grid, and independent implementation checks remain relevant before any stronger publication claim.

## Remaining requirements before a research submission

- Obtain the exact complete external review transcript with provenance and reconcile the response point by point; do not cite these summarized concerns as direct reviewer quotations.
- Complete the registered sweep over other \(b\) values, add controls and independent replication, and stress-test unknown \(p\), imperfect syndromes, and distribution shift.
- Execute the QuTiP density-matrix cross-check or explicitly remove it from any proposed evidence of validation.
- Confirm author contributions, affiliations, comparison with existing literature, and the intended claims of novelty; consider renaming the paper as an *exploratory note* if these requirements remain open.

**Conclusion:** We accept the core concerns about physical scope and missing execution evidence, and we defend transparent negative logs and model-conditional statistics as appropriate reproducibility practices. This response does not overturn a reported rejection or imply any reviewer has accepted the revisions.