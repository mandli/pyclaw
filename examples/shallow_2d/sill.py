#!/usr/bin/env python
# encoding: utf-8
r"""
2D shallow water: flow over a sill
==================================

Solve the 2D shallow water equations with
variable bathymetry:

.. :math:
    h_t + (hu)_x + (hv)_y & = 0 \\
    (hu)_t + (hu^2 + \frac{1}{2}gh^2)_x + (huv)_y & = -g h b_x \\
    (hv)_t + (huv)_x + (hv^2 + \frac{1}{2}gh^2)_y & = -g h b_y.

The bathymetry contains a gaussian hump.
are outflow.
"""

from __future__ import absolute_import
from clawpack import riemann
from clawpack import pyclaw
from clawpack.riemann.shallow_roe_with_efix_2D_constants import depth, x_momentum, y_momentum, num_eqn
import numpy as np

amplitude = 0.1  # Height of incoming wave
t_bdy = 5.       # Stop sending in waves at this time


def bathymetry(x, y):
    r2 = (x - 0.5)**2
    return -1.0 + 0.8 * np.exp(-10.0 * r2)


def wave_maker_bc(state, dim, t, qbc, auxbc, num_ghost):
    "Generate waves at left boundary as if there were a moving wall there."
    if dim.on_lower_boundary:
        qbc[0, :num_ghost, :] = qbc[0, num_ghost, :]
        t = state.t
        if t <= t_bdy:
            vwall = amplitude * (np.sin(t * np.pi / 1.5))
        else:
            vwall = 0.0
        for ibc in xrange(num_ghost - 1):
            qbc[1, num_ghost - ibc - 1, :] = 2.0 * vwall            \
                                             - qbc[1, num_ghost + ibc, :]


def setup(kernel_language='Fortran', solver_type='classic', use_petsc=False,
          outdir='./_output'):

    solver = pyclaw.ClawSolver2D(riemann.shallow_bathymetry_fwave_2D)

    # solver.bc_lower[0] = pyclaw.BC.custom
    # solver.user_bc_lower = wave_maker_bc
    solver.bc_lower[0] = pyclaw.BC.extrap
    solver.bc_upper[0] = pyclaw.BC.extrap
    solver.bc_lower[1] = pyclaw.BC.extrap
    solver.bc_upper[1] = pyclaw.BC.extrap

    solver.aux_bc_lower[0] = pyclaw.BC.extrap
    solver.aux_bc_upper[0] = pyclaw.BC.extrap
    solver.aux_bc_lower[1] = pyclaw.BC.extrap
    solver.aux_bc_upper[1] = pyclaw.BC.extrap

    my = 80
    mx = 80
    x = pyclaw.Dimension(0.0, 1.0, mx, name='x')
    y = pyclaw.Dimension(0.0, 1.0, my, name='y')
    domain = pyclaw.Domain([x, y])
    state = pyclaw.State(domain, num_eqn, num_aux=1)

    X, Y = state.p_centers
    state.aux[0, :, :] = bathymetry(X, Y)

    state.problem_data['grav'] = 1.0
    state.problem_data['dry_tolerance'] = 1.e-3
    state.problem_data['sea_level'] = 0.0

    state.q[depth, :, :] = state.problem_data['sea_level'] - state.aux[0, :, :]
    state.q[depth, :, :] += 0.1 * np.exp(-((Y-0.1)**2 + (X - 0.1)**2) / 0.05)
    state.q[x_momentum, :, :] = 0.0
    state.q[y_momentum, :, :] = 0.0

    claw = pyclaw.Controller()
    claw.tfinal = 10
    claw.solution = pyclaw.Solution(state, domain)
    claw.solver = solver
    # claw.output_style = 3
    claw.num_output_times = 40
    claw.setplot = setplot
    claw.keep_copy = True

    return claw


def surface_height(current_data):
    h = current_data.q[0, :, :]
    b = bathymetry(current_data.x, current_data.y)
    # b = -np.ones(current_data.q.shape[1:])
    return h+b


def setplot(plotdata):
    import matplotlib.pyplot as plt

    plotdata.clearfigures()  # clear any old figures,axes,items data

    # Figure for q[0]
    plotfigure = plotdata.new_plotfigure(name='Water Surface', figno=0)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Water surface'
    plotaxes.scaled = False

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = surface_height
    plotitem.pcolor_cmap = plt.get_cmap("RdBu_r")
    plotitem.pcolor_cmin = -0.1
    plotitem.pcolor_cmax = 0.1
    plotitem.add_colorbar = True

    # Figure for q[0]
    plotfigure = plotdata.new_plotfigure(name='Water Depth', figno=1)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Water depth'
    plotaxes.scaled = False

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = 0
    # plotitem.pcolor_cmap = plt.get_cmap("Rd_r")
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 1.1
    plotitem.add_colorbar = True

    return plotdata


if __name__ == "__main__":
    from clawpack.pyclaw.util import run_app_from_main
    output = run_app_from_main(setup, setplot)
