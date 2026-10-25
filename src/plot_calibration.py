#!/usr/bin/env python3
"""Plot measured Phase-2 calibration aggregate without re-running experiments."""
import argparse
import json
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',default='results/calibration.json')
    ap.add_argument('--dir',default='results/figures')
    args=ap.parse_args()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    d=json.loads(Path(args.input).read_text(encoding='utf-8'))
    rows=d['results']
    n=[str(r['N']) for r in rows]
    fractions=[r['oracle_branch_fraction']*100 for r in rows]
    lows=[r['oracle_branch_wilson95'][0]*100 for r in rows]
    highs=[r['oracle_branch_wilson95'][1]*100 for r in rows]
    ler=[r['average_exact_logical_error_rate']*100 for r in rows]
    ler_low=[r['average_exact_logical_error_rate_wilson_derived95'][0]*100 for r in rows]
    ler_high=[r['average_exact_logical_error_rate_wilson_derived95'][1]*100 for r in rows]
    dest=Path(args.dir); dest.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(8,4.5))
    ax.errorbar(n,fractions,yerr=[[max(0.0,x-y) for x,y in zip(fractions,lows)],[max(0.0,y-x) for x,y in zip(fractions,highs)]],
                fmt='o-',capsize=4,label='Oracle MAP branch selected (Wilson 95% CI)')
    ax.axhline(95,linestyle='--',color='gray',label='Registered H1 criterion: 95%')
    ax.set(xlabel='Calibration sample size N',ylabel='Oracle branch selection (%)',ylim=(-5,105),
           title='QEC-R01 Phase 2 — decoder branch selection (b = 0.04)')
    ax.grid(alpha=.25); ax.legend(loc='lower right');fig.tight_layout()
    f1=dest/'calibration_branch_selection.png';fig.savefig(f1,dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.5))
    ax.errorbar(n,ler,yerr=[[max(0.0,x-y) for x,y in zip(ler,ler_low)],[max(0.0,y-x) for x,y in zip(ler,ler_high)]],
                fmt='o-',capsize=4,label='Calibrated MAP mean exact logical error (95% CI)')
    ax.axhline(d['exact_minimum_weight_LER']*100,linestyle='--',color='gray',label='Minimum-weight baseline')
    ax.axhline(d['exact_oracle_MAP_LER']*100,linestyle=':',color='black',label='Oracle MAP limit')
    ax.set(xlabel='Calibration sample size N',ylabel='Logical X-error rate (%)',
           title='QEC-R01 Phase 2 — average exact LER after calibration (b = 0.04)')
    ax.grid(alpha=.25);ax.legend();fig.tight_layout()
    f2=dest/'calibration_logical_error.png';fig.savefig(f2,dpi=160);plt.close(fig)
    print('FIGURES:',f1,f2)

if __name__=='__main__': main()
