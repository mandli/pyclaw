
#include <p4est_to_p8est.h>

#define pyclaw_p4est_t          pyclaw_p8est_t
#define pyclaw_p4est_new	pyclaw_p8est_new
#define pyclaw_p4est_destroy	pyclaw_p8est_destroy

#define pyclaw_p4est_leaf_t	pyclaw_p8est_leaf_t
#define pyclaw_p4est_leaf_next	pyclaw_p8est_leaf_next
#define pyclaw_p4est_leaf_first	pyclaw_p8est_leaf_first

#include "pyclaw_p4est_2d.c"
