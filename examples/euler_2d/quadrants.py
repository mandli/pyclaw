#!/usr/bin/env python
# encoding: utf-8
"""
2D Euler Riemann problem
================================

Solve the Euler equations of compressible fluid dynamics:

.. math::
    \rho_t + (\rho u)_x + (\rho v)_y & = 0 \\
    (\rho u)_t + (\rho u^2 + p)_x + (\rho uv)_y & = 0 \\
    (\rho v)_t + (\rho uv)_x + (\rho v^2 + p)_y & = 0 \\
    E_t + (u (E + p) )_x + (v (E + p))_y & = 0.

Here :math:`\rho` is the density, (u,v) is the velocity, and E is the total energy.
The initial condition is one of the 2D Riemann problems from the paper of
Liska and Wendroff.
"""

from clawpack import pyclaw
from clawpack import riemann

solver = pyclaw.ClawSolver2D(riemann.euler_4wave_2D)
solver.all_bcs = pyclaw.BC.extrap

domain = pyclaw.Domain([0.,0.],[1.,1.],[100,100])
solution = pyclaw.Solution(solver.num_eqn,domain)
gamma = 1.4
solution.problem_data['gamma']  = gamma
solver.dimensional_split = False
solver.transverse_waves = 2

# Set initial data
xx,yy = domain.grid.p_centers
l = xx<0.8; r = xx>=0.8; b = yy<0.8; t = yy>=0.8
solution.q[0,...] = 1.5*r*t + 0.532258064516129*l*t + 0.137992831541219*l*b + 0.532258064516129*r*b
u = 0.*r*t + 1.206045378311055*l*t + 1.206045378311055*l*b + 0.*r*b
v = 0.*r*t + 0.*l*t + 1.206045378311055*l*b + 1.206045378311055*r*b
p = 1.5*r*t + 0.3*l*t + 0.029032258064516*l*b + 0.3*r*b
solution.q[1,...] = solution.q[0,...] * u
solution.q[2,...] = solution.q[0,...] * v
solution.q[3,...] = 0.5*solution.q[0,...]*(u**2+v**2) + p/(gamma-1.)

claw = pyclaw.Controller()
claw.tfinal = 0.8
claw.solution = solution
claw.solver = solver

status = claw.run()

#pyclaw.plot.interactive_plot()
