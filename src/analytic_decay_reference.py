#!/usr/bin/env python3
"""Analytical Lindblad reference ONLY; NOT a QuTiP simulation."""
import argparse
import math
from pathlib import Path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--figure',default='results/figures/analytic_population_decay_NOT_QUTIP.png')
    args=parser.parse_args()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    gamma=.4
    t=[i*.05 for i in range(161)]
    single=[math.exp(-gamma*x) for x in t]
    triple=[math.exp(-3*gamma*x) for x in t]
    fig,ax=plt.subplots(figsize=(8,4.5))
    ax.plot(t,single,label='Analytical single-qubit P(1) = exp(-gamma t)')
    ax.plot(t,triple,label='Analytical joint P(111) = exp(-3 gamma t)')
    ax.set(xlabel='Time (arbitrary units)',ylabel='Population',ylim=(-.02,1.02),
           title='Analytic damping reference — QuTiP NOT RUN')
    ax.grid(alpha=.25);ax.legend();fig.tight_layout()
    dest=Path(args.figure);dest.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(dest,dpi=160);plt.close(fig)
    print(f'ANALYTIC ONLY figure: {dest} | gamma={gamma}')

if __name__=='__main__':main()
