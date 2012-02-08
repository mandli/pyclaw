
import pyclaw
import amr
from ctypes import *

# Wrap p4est composite structures with ctypes
class pyclaw_sc_array (Structure):
        _fields_ = [("elem_size", c_ulonglong),
                    ("elem_count", c_ulonglong),
                    ("byte_alloc", c_longlong),
                    ("array", c_void_p)]
pyclaw_sc_array_pointer = POINTER (pyclaw_sc_array)
class pyclaw_mesh (Structure):
        _fields_ = [("local_num_vertices", c_int),
                    ("local_num_quadrants", c_int),
                    ("ghost_num_quadrants", c_int),
                    ("vertices", c_void_p),
                    ("quad_to_vertex", POINTER (c_int)),
                    ("ghost_to_proc", POINTER (c_int)),
                    ("ghost_to_index", POINTER (c_int)),
                    ("quad_to_quad", POINTER (c_int)),
                    ("quad_to_face", POINTER (c_byte)),
                    ("quad_to_half", pyclaw_sc_array_pointer)]
pyclaw_mesh_pointer = POINTER (pyclaw_mesh)
class pyclaw_pp (Structure):
        _fields_ = [("P4EST_DIM", c_int),       # space dimension
                    ("P4EST_HALF", c_int),      # small faces   2^(dim - 1)
                    ("P4EST_FACES", c_int),     # faces around  2 * dim
                    ("P4EST_CHILDREN", c_int),  # children      2^dim
                    ("conn", c_void_p),
                    ("p4est", c_void_p),
                    ("ghost", c_void_p),
                    ("mesh", pyclaw_mesh_pointer)]
pyclaw_pp_pointer = POINTER (pyclaw_pp)

def pyclaw_pp_get_num_leaves (pp):
        return pp.contents.mesh.contents.local_num_quadrants

# Wrap leaf iterator with ctypes
class pyclaw_leaf (Structure):
        _fields_ = [("pp", pyclaw_pp_pointer),
                    ("level", c_int),
                    ("which_tree", c_int),
                    ("which_quad", c_int),
                    ("total_quad", c_int),
                    ("tree", c_void_p),
                    ("quad", c_void_p),
                    ("lowerleft", c_double * 3),
                    ("upperright", c_double * 3)]
pyclaw_leaf_pointer = POINTER (pyclaw_leaf)

# Dynamically link in the pyclaw p4est interface
libp4est = CDLL ("pyclaw_p4est.so")
libp4est.pyclaw_p4est_new.restype = pyclaw_pp_pointer;
libp4est.pyclaw_p4est_new.argtype = c_int;
libp4est.pyclaw_p4est_leaf_first.restype = pyclaw_leaf_pointer;
libp4est.pyclaw_p4est_leaf_next.restype = pyclaw_leaf_pointer;

# subclass Domain to handle multiple patches presented by p4est
class p4est_Domain (pyclaw.geometry.Domain):

        # Expect geom to be a list of 2 dimensions (2D here for now).
   def __init__ (self, geom):
       # TODO: Handle multiple patches in a single domain (use multiple trees)
       # Initialize MPI. TODO: Do this in a generic routine
       libp4est.pyclaw_MPI_Init ()
       
       # Create a 2D p4est internal state on a square
       initial_level = 1
       self.pp = libp4est.pyclaw_p4est_new (initial_level)
       self.num_leaves = pyclaw_pp_get_num_leaves (self.pp)
       
       # Number of faces of a leaf (4 in 2D, 6 in 3D)
       P4EST_FACES = self.pp.contents.P4EST_FACES
       
       # Mesh is the lookup table for leaf neighbors
       mesh = self.pp.contents.mesh
       
       # Use the leaf iterator to loop over all leafs
       # If only a loop over leaf indices is needed,
       # do instead: for leafindex in range (0, self.num_leaves)
       leaf = libp4est.pyclaw_p4est_leaf_first (self.pp)
       self.patches = []
       patch_counter = 0
       while (leaf):
           patch_counter += 1
           
           # This is a demonstration to show off the structure
           print "Py leaf level", leaf.contents.level, \
           "tree", leaf.contents.which_tree, \
           "tree_leaf", leaf.contents.which_quad, \
           "local_leaf", leaf.contents.total_quad
           for nface in range (self.pp.contents.P4EST_FACES):
               print "Py leaf face", nface, "leaf", \
           
           mesh.contents.quad_to_quad [P4EST_FACES * leaf.contents.total_quad + nface]
           
           x = pyclaw.Dimension('x',  leaf.contents.lowerleft[0] , leaf.contents.upperright[0] , 64)
           y = pyclaw.Dimension('y', leaf.contents.lowerleft[1] , leaf.contents.upperright[1], 64)
           
           patch = pyclaw.geometry.Patch ([x, y])
           patch.patch_index = leaf.contents.total_quad
           self.patches.append (patch)
           leaf = libp4est.pyclaw_p4est_leaf_next (leaf)
       
   def __del__ (self):
           libp4est.pyclaw_p4est_destroy (self.pp)

           # Finalize MPI. TODO: Do this in a generic routine
           libp4est.pyclaw_MPI_Finalize ()
    
