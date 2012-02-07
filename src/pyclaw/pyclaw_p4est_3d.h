
#include <p8est_mesh.h>

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

pyclaw_p8est_t * pyclaw_p8est_new (void);
void             pyclaw_p8est_destroy (pyclaw_p8est_t * pp);
