
import pyclaw
from ctypes import *

# Dynamically link in the pyclaw p4est interface
libp4est = CDLL ("pyclaw_p4est.so")

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
		    ("quad_to_vertex", c_void_p),
		    ("ghost_to_proc", c_void_p),
		    ("ghost_to_index", c_void_p),
		    ("quad_to_quad", c_void_p),
		    ("quad_to_face", c_void_p),
		    ("quad_to_half", pyclaw_sc_array_pointer)]
pyclaw_mesh_pointer = POINTER (pyclaw_mesh)
class pyclaw_pp (Structure):
	_fields_ = [("conn", c_void_p),
		    ("p4est", c_void_p),
		    ("ghost", c_void_p),
		    ("mesh", pyclaw_mesh_pointer),
		    ("mesh_quad_to_half_num", c_int),
		    ("mesh_quad_to_half_entries", c_void_p),
		    ("test_number", c_int)]
pyclaw_pp_pointer = POINTER (pyclaw_pp)

# subclass Domain to handle multiple patches presented by p4est
class p4est_Domain (pyclaw.geometry.Domain):

	# Expect geom to be a list of 2 dimensions (2D here for now).
	def __init__ (self, geom):
		# Initialize MPI. TODO: Do this in a generic routine
		libp4est.pyclaw_MPI_Init ()

		# Create a 2D p4est internal state on a square
		pyclaw_p4est_new = libp4est.pyclaw_p4est_new
		pyclaw_p4est_new.restype = pyclaw_pp_pointer;
		self.pp = pyclaw_p4est_new ()
		mesh = self.pp.contents.mesh.contents
		self.local_num_patches = mesh.local_num_quadrants

		print "A test number: ", self.pp.contents.test_number
		print "Number of elements: ", self.local_num_patches

	#	self.grids = []
	#	for i in range (self.local_num_patches):
	# 		# TODO: change coordinates for subpatch by geom
	# 		x = pyclaw.Dimension('x', -1.0, 1.0, 200)
	# 		y = pyclaw.Dimension('y', -1.0, 1.0, 200)
	#
	# 		self.grids.append (Grid ([x, y]))

	def __del__ (self):
		libp4est.pyclaw_p4est_destroy (self.pp)

		# Finalize MPI. TODO: Do this in a generic routine
		libp4est.pyclaw_MPI_Finalize ()

# This is code for testing
x = pyclaw.Dimension('x', 0.0, 1.0, 64)
y = pyclaw.Dimension('y', 0.0, 1.0, 64)
domain = p4est_Domain ([x, y])
