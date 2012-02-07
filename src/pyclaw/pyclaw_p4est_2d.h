
#include <p4est_mesh.h>

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

pyclaw_p4est_t * pyclaw_p4est_new (void);
void             pyclaw_p4est_destroy (pyclaw_p4est_t * pp);
