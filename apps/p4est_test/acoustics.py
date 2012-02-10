#!/usr/bin/env python
# encoding: utf-8

import numpy as np

def acoustics2D(iplot=False,htmlplot=False,parallel=False,outdir='./_output',solver_type='classic'):
    r"""
    Example python script for solving the 2d acoustics equations running with
    p4est.
    """

    import pyclaw
    import pyclaw.amr as amr
    import pyclaw.p4est as p4est

    sub_solver=pyclaw.ClawSolver2D()
    sub_solver.dimensional_split=False

    sub_solver.num_waves = 2
    sub_solver.limiters = pyclaw.limiters.tvd.MC

    solver = amr.AMRSolver()
    solver.sub_solver = sub_solver
    # solver.dt_variable = False
    solver.bc_lower[0]=pyclaw.BC.wall
    solver.bc_upper[0]=pyclaw.BC.extrap
    solver.bc_lower[1]=pyclaw.BC.wall
    solver.bc_upper[1]=pyclaw.BC.extrap

    # Initialize domain
    mx=100; my=100
    num_eqn = 3
    x = pyclaw.Dimension('x',0.0,1.0,mx)
    y = pyclaw.Dimension('y',0.0,1.0,my)
    domain = p4est.p4est_Domain([x,y])
    solution = pyclaw.Solution(domain,num_eqn,0)

    rho = 1.0
    bulk = 4.0
    cc = np.sqrt(bulk/rho)
    zz = rho*cc
    for state in solution.states:
        state.problem_data['rho']= rho
        state.problem_data['bulk']=bulk
        state.problem_data['zz']= zz
        state.problem_data['cc']=cc

        grid = state.grid
        Y,X = np.meshgrid(grid.y.centers,grid.x.centers)
        r = np.sqrt((X-0.5)**2 + (Y-0.5)**2) / 0.5
        width=0.2
        state.q[0,:,:] = (np.abs(r-0.5)<=width)*(1.+np.cos(np.pi*(r-0.5)/width))
        state.q[1,:,:] = 0.
        state.q[2,:,:] = 0.

    claw = pyclaw.Controller()
    claw.keep_copy = True
    claw.solution = solution
    claw.solver = solver
    claw.dt_initial = 0.001
    claw.outdir = outdir

    # Solve
    claw.outstyle = 1
    claw.tfinal = 0.02
    claw.num_output_times = 10
    claw.run()
    
    if htmlplot:  pyclaw.plot.html_plot(outdir=outdir,file_format=claw.output_format)
    if iplot:     pyclaw.plot.interactive_plot(outdir=outdir,file_format=claw.output_format)



if __name__=="__main__":
    import sys
    from pyclaw.util import run_app_from_main
    output = run_app_from_main(acoustics2D)
