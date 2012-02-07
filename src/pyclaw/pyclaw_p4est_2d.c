
#ifndef P4_TO_P8
#include "pyclaw_p4est_2d.h"
#else
#include "pyclaw_p4est_3d.h"
#endif

pyclaw_p4est_t *
pyclaw_p4est_new (void)
{
  pyclaw_p4est_t * pp;

  pp = SC_ALLOC (pyclaw_p4est_t, 1);
#ifndef P4_TO_P8
  pp->conn = p4est_connectivity_new_unitsquare ();
#else
  pp->conn = p8est_connectivity_new_unitcube ();
#endif
  pp->p4est = p4est_new (MPI_COMM_WORLD, pp->conn, 0, NULL, NULL);
  pp->ghost = p4est_ghost_new (pp->p4est, P4EST_CONNECT_FULL);
  pp->mesh = p4est_mesh_new (pp->p4est, pp->ghost, P4EST_CONNECT_FULL);
  pp->mesh_quad_to_half_num =
    (p4est_locidx_t) pp->mesh->quad_to_half->elem_count;
  pp->mesh_quad_to_half_entries =
    (p4est_locidx_t *) pp->mesh->quad_to_half->array;
#ifndef P4_TO_P8
  pp->test_number = 22222;
#else
  pp->test_number = 33333;
#endif

  return pp;
}

void
pyclaw_p4est_destroy (pyclaw_p4est_t * pp)
{
  p4est_mesh_destroy (pp->mesh);
  p4est_ghost_destroy (pp->ghost);
  p4est_destroy (pp->p4est);
  p4est_connectivity_destroy (pp->conn);

  SC_FREE (pp);
}
