#!/usr/bin/env python

r""""""

import pyclaw

class AMRSolver(pyclaw.solver.Solver):
    
    def __init__(self,claw_package=None):
        
        self._sub_solvers = []
        self.sub_solver = None
        # TODO: This does not belong here, temporary!
        self.num_dim = 2
        super(AMRSolver,self).__init__(claw_package)
        
    def setup(self,solution):
        r"""Setup bc arrays"""
        # TODO: Allow the specification of a sub_solver manually
        self._sub_solvers = [self.sub_solver] * len(solution.domain.patches)
        
        if len(self._sub_solvers) != len(solution.domain.patches):
            raise Exception("Number of sub-solvers != number of patches!")

        for (i,state) in enumerate(solution.states):
            # Setup each sub solver
            self._sub_solvers[i].setup(pyclaw.Solution(state))
            self._sub_solvers[i].allocate_bc_arrays(state)
            
            # Set appropriate time stepping
            self._sub_solvers[i].cfl_max = self.cfl_max
            self._sub_solvers[i].cfl_desired = self.cfl_desired
            
    
    def backup_solution(self,solution):
        r"""Backup current solution for variable time stepping rejection."""
        for (i,state) in enumerate(solution.states):
            self._sub_solvers[i].backup_solution(pyclaw.Solution(state))
    
        
    def recall_backup(self,solution):
        r"""Replace the solution with the backuped data."""
        for (i,state) in enumerate(solution.states):
            self._sub_solvers[i].recall_backup()

    
    def step(self,solution):
        
        # Loop through all states on the solution given
        for (k,state) in enumerate(solution.states):
            mesh = solution.domain.pp.contents.mesh

            # Make sure nothing is quadratic in the number of grids EVER
            for (i,dimension) in enumerate(state.patch.dimensions):
                lower_nface = 2*i
                upper_nface = 2*i + 1
                
                # Check lower dimension boundary
                neighbor_lower_quad = mesh.contents.quad_to_quad[
                                          solution.domain.pp.contents.P4EST_FACES 
                                        * state.patch.patch_index + lower_nface]
                if not (neighbor_lower_quad == state.patch.patch_index):
                    self._sub_solvers[k].bc_lower[i] = 4
                    self._sub_solvers[k].bc_lower_neighbor[i] = self._sub_solvers[neighbor_lower_quad].qbc
                    self._sub_solvers[k].aux_bc_lower_neighbor[i] = self._sub_solvers[neighbor_lower_quad].auxbc
                else:
                    self._sub_solvers[k].bc_lower[i] = self.bc_lower[i]
                    self._sub_solvers[k].bc_lower_neighbor[i] = None
                    self._sub_solvers[k].aux_bc_lower_neighbor[i] = None
                    
                # Check upper dimension boundary
                neighbor_upper_quad = mesh.contents.quad_to_quad[
                                          solution.domain.pp.contents.P4EST_FACES 
                                        * state.patch.patch_index + upper_nface]
                if not (neighbor_upper_quad == state.patch.patch_index):
                    self._sub_solvers[k].bc_upper[i] = 4
                    self._sub_solvers[k].bc_upper_neighbor[i] = self._sub_solvers[neighbor_upper_quad].qbc
                    self._sub_solvers[k].aux_bc_upper_neighbor[i] = self._sub_solvers[neighbor_upper_quad].auxbc
                else:
                    self._sub_solvers[k].bc_upper[i] = self.bc_upper[i]
                    self._sub_solvers[k].bc_upper_neighbor[i] = None
                    self._sub_solvers[k].aux_bc_upper_neighbor[i] = None
            
            # self.sub_solver.dt = self.dt
            self._sub_solvers[k].step(state)
            CFL
            self._sub_solvers[k].dt = self.dt
            # Not sure about this step, is this a copy?
            solution.states[k].q = state.q
            solution.states[k].aux = state.aux