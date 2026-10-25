#!/usr/bin/env python3
"""QuTiP 5.3.1: 3-qubit amplitude-damping Lindblad density-matrix experiment.

All qubits initially |111>. Each has collapse operator sqrt(gamma)*a_i,
where a = |0><1| = destroy(2). With H=0 the exact reference for each
excited-state marginal is exp(-gamma*t), and for |111> is exp(-3*gamma*t).

Requires installed qutip==5.3.1 + numpy + matplotlib.
Exit 3 if QuTiP is absent; never silently substitute analytical results.
"""
import argparse
import json
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',default='results/qutip_decay.json')
    ap.add_argument('--figure',default='results/figures/qutip_population_decay.png')
    ap.add_argument('--gamma',type=float,default=0.4)
    args=ap.parse_args()
    try:
        import qutip as qt
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError as e:
        print(f'BLOCKED: QuTiP experiment cannot run; missing dependency: {e}',flush=True)
        raise SystemExit(3)
    if qt.__version__ != '5.3.1':
        raise SystemExit(f'BLOCKED: require qutip==5.3.1, got {qt.__version__}')
    if args.gamma <= 0:
        ap.error('--gamma must be > 0')
    ident=qt.qeye(2)
    a=qt.destroy(2)
    excitation=qt.num(2)
    psi=qt.tensor(qt.basis(2,1), qt.basis(2,1), qt.basis(2,1))
    rho0=qt.ket2dm(psi)
    assert rho0.shape==(8,8) and abs(rho0.tr()-1)<1e-12
    collapse=[args.gamma**0.5*qt.tensor(*[(a if j==i else ident) for j in range(3)]) for i in range(3)]
    project_111=qt.ket2dm(psi)
    pops=[qt.tensor(*[(excitation if j==i else ident) for j in range(3)]) for i in range(3)]
    times=np.linspace(0,8,161)
    # H=zero operator with matching tensor dimensions.
    H=0*qt.tensor(ident,ident,ident)
    sim=qt.mesolve(H,rho0,times,collapse,e_ops=pops+[project_111],options={'store_states': True})
    observed=np.asarray(sim.expect,dtype=float)
    theory=np.exp(-args.gamma*times)
    max_error=float(np.max(np.abs(observed[:3,:]-theory[None,:])))
    triple_ref=np.exp(-3*args.gamma*times)
    max_joint_error=float(np.max(np.abs(observed[3,:]-triple_ref)))
    max_trace_error=max(abs(float(state.tr().real)-1) for state in sim.states)
    min_eigen=min(float(min(state.eigenenergies()).real) for state in sim.states)
    if max_error>1e-4 or max_joint_error>1e-4 or max_trace_error>1e-6 or min_eigen< -1e-7:
        raise RuntimeError('QuTiP numerical evolution failed analytical/trace/PSD checks')
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    figpath=Path(args.figure);figpath.parent.mkdir(parents=True,exist_ok=True)
    result={
        'execution_status':'PASS','qutip_version':qt.__version__,'gamma_inverse_time':args.gamma,
        'initial_state':'|111>','density_matrix_dimension':[8,8],
        'collapse_operators':'sqrt(gamma)*tensor(destroy(2),I,I) and permutations',
        'time':times.tolist(),'population_per_qubit':observed[:3,:].tolist(),
        'joint_population_111':observed[3,:].tolist(),'analytic_population_single':theory.tolist(),
        'analytic_joint_population_111':triple_ref.tolist(),
        'max_abs_error_single':max_error,'max_abs_error_joint':max_joint_error,
        'max_abs_trace_error':max_trace_error,'minimum_density_matrix_eigenvalue':min_eigen,
    }
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    fig,ax=plt.subplots(figsize=(8,5))
    ax.plot(times,observed[0,:],label='QuTiP P(qubit 0=1)',linewidth=2)
    ax.plot(times,observed[1,:],':',label='QuTiP P(qubit 1=1)')
    ax.plot(times,observed[2,:],'-.',label='QuTiP P(qubit 2=1)')
    ax.plot(times,theory,'k--',label='Analytic exp(-gamma t)',alpha=.7)
    ax.plot(times,observed[3,:],label='QuTiP P(|111>)')
    ax.set(title='Three-qubit independent amplitude damping (QuTiP 5.3.1)',xlabel='Time (arbitrary units)',ylabel='Excited population',ylim=(-.02,1.02))
    ax.grid(alpha=.3); ax.legend();fig.tight_layout();fig.savefig(figpath,dpi=170);plt.close(fig)
    print(f'QUTIP PASS | version {qt.__version__} | max single deviation={max_error:.3g} | trace deviation={max_trace_error:.3g}')
    print(f'JSON: {out} | Figure: {figpath}')

if __name__=='__main__': main()
