
import pyclaw
from ctypes import *

# Dynamically link in the pyclaw p4est interface
libp4est = CDLL ("pyclaw_p4est.so")

# Wrap p4est composite structures with ctypes
class pyclaw_p4est (Structure):
	_fields_ = [("conn", c_void_p),
		    ("p4est", c_void_p),
		    ("ghost", c_void_p),
		    ("mesh", c_void_p),
		    ("mesh_quad_to_half_num", c_int),
		    ("mesh_quad_to_half_entries", c_void_p),
		    ("test_number", c_int)]
pyclaw_p4est_pointer = POINTER (pyclaw_p4est)

# subclass Domain to handle multiple patches presented by p4est
class p4est_Domain (pyclaw.geometry.Domain):

	# Expect geom to be a list of 2 dimensions (2D here for now).
	def __init__ (self, geom):
		# Initialize MPI. TODO: Do this in a generic routine
		libp4est.pyclaw_MPI_Init ()

		# Create a 2D p4est internal state on a square
		pyclaw_p4est_new = libp4est.pyclaw_p4est_new
		pyclaw_p4est_new.restype = pyclaw_p4est_pointer;
		self.pp = pyclaw_p4est_new ()
		print "A test number: ", self.pp.contents.test_number

	# 	self.patches = []
	# 	for () :
	# 		# TODO: change coordinates for subpatch by geom
	# 		x = pyclaw.Dimension('x', -1.0, 1.0, 200)
	# 		y = pyclaw.Dimension('y', -1.0, 1.0, 200)
	#
	# 		self.patches.append (Patch ([x, y]))

	def __del__ (self):
		libp4est.pyclaw_p4est_destroy (self.pp)

		# Finalize MPI. TODO: Do this in a generic routine
		libp4est.pyclaw_MPI_Finalize ()

# This is code for testing
x = pyclaw.Dimension('x', 0.0, 1.0, 64)
y = pyclaw.Dimension('y', 0.0, 1.0, 64)
domain = p4est_Domain ([x, y])
