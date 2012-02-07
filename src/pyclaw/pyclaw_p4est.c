
#include <p4est_mesh.h>
#include <p8est_mesh.h>

/* TODO: This should be called elsewhere in a more appropriate place */
void
pyclaw_MPI_Init (void)
{
  int argc;
  char **argv;

  argc = 0;
  argv = NULL;

  MPI_Init (&argc, &argv);
}

/* TODO: This should be called elsewhere in a more appropriate place */
void
pyclaw_MPI_Finalize (void)
{
  MPI_Finalize ();
}

/* 2D p4est routines */

typedef struct pyclaw_p4est {
  p4est_connectivity_t * conn;
  p4est_t * p4est;
  p4est_ghost_t * ghost;
  p4est_mesh_t * mesh;
  /* these two variables expose members of mesh->quad_to_half */
  p4est_locidx_t mesh_quad_to_half_num;
  p4est_locidx_t * mesh_quad_to_half_entries;
  int test_number;
}
pyclaw_p4est_t;

pyclaw_p4est_t *
pyclaw_p4est_new (void)
{
  pyclaw_p4est_t * pp;

  pp = SC_ALLOC (pyclaw_p4est_t, 1);
  pp->conn = p4est_connectivity_new_unitsquare ();
  pp->p4est = p4est_new (MPI_COMM_WORLD, pp->conn, 0, NULL, NULL);
  pp->ghost = p4est_ghost_new (pp->p4est, P4EST_CONNECT_FULL);
  pp->mesh = p4est_mesh_new (pp->p4est, pp->ghost, P4EST_CONNECT_FULL);
  pp->mesh_quad_to_half_num =
    (p4est_locidx_t) pp->mesh->quad_to_half->elem_count;
  pp->mesh_quad_to_half_entries =
    (p4est_locidx_t *) pp->mesh->quad_to_half->array;
  pp->test_number = 22222;

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

/* 3D p4est routines */

typedef struct pyclaw_p8est {
  p8est_connectivity_t * conn;
  p8est_t * p4est;
  p8est_ghost_t * ghost;
  p8est_mesh_t * mesh;
  /* these two variables expose members of mesh->quad_to_half */
  p4est_locidx_t mesh_quad_to_half_num;
  p4est_locidx_t * mesh_quad_to_half_entries;
  int test_number;
}
pyclaw_p8est_t;

pyclaw_p8est_t *
pyclaw_p8est_new (void)
{
  pyclaw_p8est_t * pp;

  pp = SC_ALLOC (pyclaw_p8est_t, 1);
  pp->conn = p8est_connectivity_new_unitcube ();
  pp->p4est = p8est_new (MPI_COMM_WORLD, pp->conn, 0, NULL, NULL);
  pp->ghost = p8est_ghost_new (pp->p4est, P4EST_CONNECT_FULL);
  pp->mesh = p8est_mesh_new (pp->p4est, pp->ghost, P4EST_CONNECT_FULL);
  pp->mesh_quad_to_half_num =
    (p4est_locidx_t) pp->mesh->quad_to_half->elem_count;
  pp->mesh_quad_to_half_entries =
    (p4est_locidx_t *) pp->mesh->quad_to_half->array;
  pp->test_number = 33333;

  return pp;
}

void
pyclaw_p8est_destroy (pyclaw_p8est_t * pp)
{
  p8est_mesh_destroy (pp->mesh);
  p8est_ghost_destroy (pp->ghost);
  p8est_destroy (pp->p4est);
  p8est_connectivity_destroy (pp->conn);

  SC_FREE (pp);
}
