# QEC-R01 — correlated X-noise in a 3-qubit repetition code

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Build Passing](https://github.com/Vahiff/qec-r01-public/actions/workflows/build-paper-pdf.yml/badge.svg)](https://github.com/Vahiff/qec-r01-public/actions/workflows/build-paper-pdf.yml)

**Project files:** [Authors and CRediT roles](AUTHORS.md) · [Release changelog](CHANGELOG.md) · [Manuscript PDF](paper/main.pdf) · [Manuscript source](paper/main.tex)

**Status:** executable **exploratory** code-capacity pilot. The primary H1 calibration condition at `b=0.04` was executed in Phase 2; generality and scientific novelty are not verified. Repository publication is **not** a peer-reviewed result.

## Model and research question

Codewords `|0_L> = |000>` and `|1_L> = |111>`, with syndrome generators `Z0 Z1` and `Z1 Z2`. Noise is `E = (Z0,Z1,Z2) XOR (B,B,0)` where each `Zi ~ Bernoulli(p)` independently, `B ~ Bernoulli(b)`, and `p = 0.02`. The **additional** paired event may cancel independent errors. Perfect syndrome measurements, one round, no Z/Y errors, leakage, faulty gates, or hardware are modeled. This is X-only protection (X-distance 3), not a distance-3 code against arbitrary Pauli noise (full quantum distance 1).

**Question:** Under what correlation rates and finite calibration sample sizes does a correlation-aware decoder beat minimum-weight decoding? This repository currently answers only an **exploratory subquestion** with known assumed `b = 0.04`: performance vs. true `b` at 0, .01, .02, .04, .08. The finite-calibration primary condition at `b=0.04` was run in Phase 2 (see `results/REPORT.md`); the full registered grid remains **NOT RUN**.

The pilot compares `minimum-weight` decoding against a syndrome-wise maximum-a-posteriori (MAP) decoder calibrated to assumed `b = 0.04`. For the ambiguous syndrome, its model's switch threshold is `b* = p(1-p) = 0.0196`. This is a **decoder decision threshold**, not a fault-tolerance threshold.

## Reproduce the pilot

Requires **Python >= 3.10**. The executed code uses the **standard library only** (no NumPy, no vectorization). On Windows PowerShell or Git Bash from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/reproduce.py
```

`scripts/reproduce.py` invokes `src/pilot.py --shots 200000 --seed 20261025`, saves `results/pilot.json`, creates `results/run.log` with UTC timestamps, elapsed duration measured with `time.perf_counter()`, stdout/stderr, return code, and SHA-256. It checks that the JSON is deterministic compared with its pre-run contents, if present. Runtime and logs will naturally vary by host; the JSON is expected to match for the same Python random sequence and script.

To run the core pilot directly:

```bash
python src/pilot.py --shots 200000 --seed 20261025 --output results/pilot.json
```

`requirements.txt` pins **QuTiP 5.3.1** for *planned* quantum-state cross-checks, **not used or tested in this pilot**; do **not** need to install it to reproduce present results. If preparing later QuTiP extensions: `python -m pip install -r requirements.txt`.

## Evidence and limitations

- `results/pilot.json`: seed, trial counts, exact eight-mask enumeration, Monte Carlo counts, and approximate paired 95% normal intervals.
- `results/run.log`: timed subprocess execution; it is **not evidence of an earlier run's timing**. This log is generated locally by this repository's script, not by GitHub Actions.
- `tests/test_pilot.py`: elementary syndrome, normalization, threshold, and deterministic simulation checks.
- Monte Carlo 1,000,000 samples are **classical pseudorandom mask draws**: 5 conditions × 200,000. They are not 1,000,000 quantum circuit simulations.
- Scientific novelty, physical gate noise, real-device behavior, and publication/peer review: **NOT VERIFIED / NOT RUN**.

No tokens, credentials or private user data are needed. Do not put secrets in this public repo. The private work repo may contain future drafts and raw evidence; public repo should only carry explicitly publishable material.

## Follow-up (4 weeks, ~40 h)

1. Lock noise model, metrics and literature; audit exact enumeration.
2. Implement calibration estimation on independent training samples and test decoder selection.
3. Run the registered `N ∈ {0,50,200,1000,5000}` × `b ∈ {0,.01,.015,.0196,.02,.025,.04,.08}` sweep with 2,000 repeats, separate evaluation, and intervals.
4. Re-run, review literature novelty, prepare plots/report and document limitations. Do not claim publication-readiness until completed.

Relevant background: [IBM repetition codes](https://quantum.cloud.ibm.com/docs/tutorials/repetition-codes), [Sivak et al., PRL 133, 150603 (2024)](https://doi.org/10.1103/PhysRevLett.133.150603), [Google Quantum AI, Nature (2024)](https://www.nature.com/articles/s41586-024-08449-y).


## Phase 2 (2026-10-25) — executed outcomes

- H1 at true `b=0.04`, `N=1000`, 2000 calibration replicates: **1995/2000 = 99.75%** selected the oracle branch; mean exact logical X-error **0.02004896** vs minimum-weight **0.039584**. Both registered descriptive criteria met in this idealized model; full `b` grid is **NOT RUN**.
- QuTiP 5.3.1 script is committed but **BLOCKED by missing package and DNS**. Analytical decay figure explicitly says `NOT_QUTIP`.
- Arbitrary `X`, `Y`, `Z` single-qubit correction via `[[3,1,3]]` is ruled out by the quantum Singleton bound; no fake `shor3_test.py` is included.
- [Phase 2 report](results/REPORT.md) · [calibration data](results/calibration.json) · [execution log](results/calibration.log) · [figures](results/figures/)
