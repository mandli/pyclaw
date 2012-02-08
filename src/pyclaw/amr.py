#!/usr/bin/env python

r""""""

import pyclaw

class AMRSolver(pyclaw.solver.Solver):
    
    def __init__(self,sub_solver,claw_package=None):
        self.num_dim = 2
        self.num_ghost = 2
        super(AMRSolver,self).__init__(claw_package)
        self._isinitialized = False
        self.qbc = []
        self.auxbc = []
        
        self.sub_solver = sub_solver
        self._isinitialized = True
        
    def setup(self,solution):
        r"""Setup bc arrays"""
        for state in solution.states:
            qbc,auxbc = self.allocate_bc_arrays(state)
            self.qbc.append(qbc)
            self.auxbc.append(auxbc)
            sol = pyclaw.Solution(state)
            self.sub_solver.setup(sol)
            
    def backup_solution(self,solution):
        r"""Backup current solution for variable time stepping rejection."""
        for (i,state) in enumerate(solution.states):
            sol = pyclaw.Solution(state)
            self.sub_solver.backup_solution(sol)
        
    def recall_backup(self,solution):
        r"""Replace the solution with the backuped data."""
        raise NotImplementedError("No recall solution ability implemented!")
        

        
    def step(self,solution):
        
        for (k,state) in enumerate(solution.states):
            mesh = solution.domain.pp.contents.mesh

            # Make sure nothing is quadratic in the number of grids EVER
            for (i,dimension) in enumerate(state.patch.dimensions):
                lower_nface = 2*i
                upper_nface = 2*i + 1
                
                neighbor_lower_quad = mesh.contents.quad_to_quad [solution.domain.pp.contents.P4EST_FACES * state.patch.patch_index + lower_nface]
                if not (neighbor_lower_quad == state.patch.patch_index):
                    self.sub_solver.bc_lower[i] = 4
                    self.sub_solver.bc_lower_neighbor[i] = self.qbc[neighbor_lower_quad]
                else:
                    self.sub_solver.bc_lower[i] = self.bc_lower[i]
                neighbor_upper_quad = mesh.contents.quad_to_quad [solution.domain.pp.contents.P4EST_FACES * state.patch.patch_index + upper_nface]
                if not (neighbor_upper_quad == state.patch.patch_index):
                    self.sub_solver.bc_upper[i] = 4
                    self.sub_solver.bc_upper_neighbor[i] = self.qbc[neighbor_upper_quad]
                else:
                    self.sub_solver.bc_upper[i] = self.bc_upper[i]
            
            sol = pyclaw.Solution(state)
            self.sub_solver.qbc = self.qbc[k]
            self.sub_solver.dt = self.dt
            self.sub_solver.step(sol)
            self.dt = self.sub_solver.dt
            solution.states[k].q = sol.state.q