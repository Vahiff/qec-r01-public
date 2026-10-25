# Response to Reviewers — provisional summary

**Author:** Vahif Khalilov  
**Source:** [`paper/REBUTTAL.md`](paper/REBUTTAL.md). The three themes below were summarized by the repository owner, **not authenticated as verbatim quotations by a numbered "Reviewer 2"**. This is a provisional response, pending the full review text.

| Reviewer 2 Comment (owner-summarized theme) | Our Response & Location in Manuscript |
|---|---|
| **3-qubit scope:** A three-qubit repetition code cannot establish general fault-tolerant quantum computation. | **Agree.** The model corrects X-only errors with perfect syndrome extraction and no gates, hardware or Y/Z correction. See `paper/main.tex`: Abstract; Methods; **Limitations and Discussion**. |
| **QuTiP failure:** The proposed density-matrix experiment did not execute because dependency installation was blocked. | **Agree about missing evidence.** We explicitly log the missing package/DNS failure and do not report invented results. This is an environmental blocker, **not** validation of the proposed extension. See **Limitations and Discussion**, `results/qutip_install.log`, `results/qutip_run.log`. |
| **Sample size:** Calibration uses 2,000 replicates. | **Clarification.** The model-conditional branch-selection probability is an exact binomial tail; 2,000 Monte Carlo replicates cross-check the algorithm's estimated selection frequency. Precision does not extend to device-level rare failures. See **Methods**, **Results**, `results/calibration.json`. |

**Residual:** Complete review transcript NOT VERIFIED; independent quantum-hardware and QuTiP tests NOT RUN. This response must not be characterized as accepted peer review.
