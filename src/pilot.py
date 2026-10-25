#!/usr/bin/env python3
"""QEC-R01: 3-qubit bit-flip code under independent + paired X errors.

Code space: |000>, |111>; stabilizers Z0Z1 and Z1Z2.
X-distance is 3; full quantum distance is 1 because Z errors are uncorrected.
For a classical X-error bit mask e, syndrome is H e (mod 2).
Physical noise: e = z XOR (110 if B else 000), where
z_i ~ Bernoulli(p) independently; B ~ Bernoulli(b).

Assumptions: perfect stabilizer readout; one error round; known noise model;
no circuit-level gate faults, leakage, or Z errors. This is a code-capacity
proof-of-concept, not a fault-tolerant hardware demonstration.

Requires Python 3.10+; no third-party dependencies.
"""
import argparse
import json
import math
import random
from pathlib import Path

BURST = 0b011   # mask of qubits 0 and 1, i.e. X0 X1
MASK = 0b111


def syndrome(e):
    return (((e >> 0) ^ (e >> 1)) & 1, ((e >> 1) ^ (e >> 2)) & 1)


def weight(e):
    return e.bit_count()


def prob_mask(e, p, b):
    def independent(z):
        w = weight(z)
        return (p ** w) * ((1 - p) ** (3 - w))
    return (1 - b) * independent(e) + b * independent(e ^ BURST)


def decode_table(p, assumed_b):
    table = {}
    for s0 in (0, 1):
        for s1 in (0, 1):
            s = (s0, s1)
            candidates = [e for e in range(8) if syndrome(e) == s]
            assert len(candidates) == 2
            # Tie-break minimizes Hamming weight, then mask order.
            table[s] = max(candidates, key=lambda e: (prob_mask(e,p,assumed_b), -weight(e), -e))
    return table


def min_weight_table():
    table = {}
    for e in range(8):
        s = syndrome(e)
        if s not in table or weight(e) < weight(table[s]):
            table[s] = e
    return table


def logical_failure(e, correction):
    assert syndrome(e) == syndrome(correction)
    residual = e ^ correction
    assert residual in (0, MASK)
    return int(residual == MASK)


def exact_failure_rate(p, b, table):
    return sum(prob_mask(e, p, b) * logical_failure(e, table[syndrome(e)]) for e in range(8))


def monte_carlo(p, b, n, seed, baseline, informed):
    rng = random.Random(seed)
    n_base = n_info = n_improved = n_worsened = 0
    for _ in range(n):
        e = sum((1 << i) for i in range(3) if rng.random() < p)
        if rng.random() < b:
            e ^= BURST
        s = syndrome(e)
        fb = logical_failure(e, baseline[s])
        fi = logical_failure(e, informed[s])
        n_base += fb
        n_info += fi
        n_improved += (fb == 1 and fi == 0)
        n_worsened += (fb == 0 and fi == 1)
    difference = (n_base - n_info) / n
    # Paired normal-approximation interval (pilot, not a confidence guarantee).
    second_moment = (n_improved + n_worsened) / n
    se = math.sqrt(max(0.0, second_moment - difference * difference) / n)
    return {
        'shots': n,
        'failures_min_weight': n_base,
        'failures_correlated_MAP': n_info,
        'empirical_LER_min_weight': n_base / n,
        'empirical_LER_correlated_MAP': n_info / n,
        'empirical_improvement_pp': 100 * difference,
        'improvement_95pct_approx_CI_pp': [100*(difference - 1.96*se), 100*(difference + 1.96*se)],
        'discordant_shots_baseline_worse': n_improved,
        'discordant_shots_informed_worse': n_worsened,
    }


def run(shots, seed):
    p = 0.02
    assumed_b = 0.04
    burst_sweep = [0, 0.01, 0.02, 0.04, 0.08]
    baseline = min_weight_table()
    informed = decode_table(p, assumed_b)
    for s in baseline:
        assert syndrome(baseline[s]) == s
        assert syndrome(informed[s]) == s
    for b in burst_sweep:
        assert abs(sum(prob_mask(e,p,b) for e in range(8))-1) < 1e-12
    assert informed[syndrome(BURST)] == BURST
    assert baseline[syndrome(BURST)] != BURST

    results = []
    for ix, b in enumerate(burst_sweep):
        eb = exact_failure_rate(p,b,baseline)
        ei = exact_failure_rate(p,b,informed)
        mc = monte_carlo(p,b,shots,seed+ix,baseline,informed)
        # Statistical tolerance rather than unrealistic exact match requirement.
        assert abs(mc['empirical_LER_min_weight'] - eb) < 0.003
        assert abs(mc['empirical_LER_correlated_MAP'] - ei) < 0.003
        results.append({'true_pair_burst_rate':b,
                        'exact_LER_min_weight':eb,
                        'exact_LER_correlated_MAP':ei,
                        'exact_improvement_pp':100*(eb-ei),
                        **mc})

    threshold = p * (1-p)
    assert abs(threshold - .0196) < 1e-12
    # Check algebraic threshold in dominant ambiguous syndrome {001, 110}.
    for b in (.005,.015,.04,.08):
        prefers_pair = prob_mask(BURST,p,b) > prob_mask(0b100,p,b)
        assert prefers_pair == (b > threshold)

    return {
        'title': 'QEC-R01 paired X burst pilot',
        'code': '3-qubit repetition code (X-distance 3, full quantum distance 1)',
        'p_independent_flip_each_qubit':p,
        'assumed_burst_rate_for_MAP':assumed_b,
        'threshold_burst_rate_for_ambiguous_syndrome':threshold,
        'seed':seed,
        'shots_per_condition':shots,
        'baseline_table':{''.join(map(str,k)):format(v,'03b') for k,v in baseline.items()},
        'informed_table':{''.join(map(str,k)):format(v,'03b') for k,v in informed.items()},
        'results':results,
        'status':'run and validated against exact enumeration; toy code-capacity model',
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shots',type=int,default=200_000)
    ap.add_argument('--seed',type=int,default=20261025)
    ap.add_argument('--output',default='qec_r01_pilot_results.json')
    args = ap.parse_args()
    if args.shots <= 0:
        ap.error('--shots must be positive')
    report = run(args.shots,args.seed)
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('QEC-R01 | tests PASS | code-capacity toy model')
    print('p=0.0200, decoder assumes burst b=0.0400, analytic threshold b*=0.0196')
    print('b_true   exact_baseline  exact_MAP  gain_pp  MC_gain_pp  95%CI_gain_pp')
    for r in report['results']:
        lo,hi=r['improvement_95pct_approx_CI_pp']
        print(f"{r['true_pair_burst_rate']:6.3f}   "
              f"{r['exact_LER_min_weight']:13.6f}  "
              f"{r['exact_LER_correlated_MAP']:9.6f}  "
              f"{r['exact_improvement_pp']:7.3f}  "
              f"{r['empirical_improvement_pp']:10.3f}  "
              f"[{lo:6.3f},{hi:6.3f}]")
    print('JSON:',args.output)

if __name__ == '__main__':
    main()
