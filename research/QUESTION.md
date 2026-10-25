# QEC-R01 registered research question (Step 2)

Date: 2026-10-25. **Status: PROTOCOL LOCKED; CONFIRMATORY EXPERIMENT NOT RUN.**

**Question:** With an independent Pauli-X flip probability `p=.02` and additional paired flip `X0X1` probability `b`, what finite size `N` of independent calibration measurements is required for a correlation-aware MAP decoder to outperform minimum-weight decoding on a three-qubit bit-flip repetition code?

**Noise:** `E=(Z0,Z1,Z2) XOR (B,B,0)`, `Zi~Bernoulli(p)` independently, `B~Bernoulli(b)` independently. Idealized one-round code-capacity model; perfect measurement; no non-X noise. Full quantum-code distance is 1.

**Decoder:** Minimum-weight baseline; MAP decoder assumes `b_hat`. For each syndrome pick the mask maximizing its model probability, tie-breaking to minimum weight. Perfect-knowledge MAP provides oracle benchmark. The ambiguous-syndrome decision switches at `b_hat > p(1-p)=0.0196`.

**Calibration:** prepare known `|000>` samples, measure first qubit after noise; `q0 = mean(E0)` and `b_hat=clip((q0-p)/(1-2p), 0, 0.08)` for known `p`. For `N=0`, use minimum-weight. Independent calibrations and evaluation streams. This assumes destructively measurable known states, not access to physical errors in unknown logical memory.

**Primary falsifiable hypothesis H1:** at `p=.02`, true `b=.04`, `N=1000` calibration samples, 2000 independent calibration replicates: (i) the decoder selects the oracle's ambiguous-syndrome correction >=95% of replicates and (ii) its mean exact logical X failure rate is smaller than the minimum-weight baseline. H0: either condition fails.

**Registered grid:** `b=[0,.01,.015,.0196,.02,.025,.04,.08]`; `N=[0,50,200,1000,5000]`; 2000 calibration replicates each. Evaluate eight-mask exact failure rate, calibrated branch choice, and uncertainty; reserve separate random evaluation draws for independent Monte Carlo validation. Store seeds and versions before execution.

**Scientific status:** Existing work investigates correlated noise and optimized decoder priors; originality of this precise study **NOT VERIFIED**. The archived `src/pilot.py` is **exploratory only**, does not evaluate H1, and must not be substituted for its confirmatory test. No gate-fault simulation or real-device verification has been performed.
