
#include <p8est_mesh.h>

/*** COMPLETE INTERNAL STATE OF P4EST ***/

typedef struct pyclaw_p8est {
  p8est_connectivity_t * conn;
  p8est_t * p4est;
  p8est_ghost_t * ghost;
  p8est_mesh_t * mesh;
  int test_number;
}
pyclaw_p8est_t;

pyclaw_p8est_t * pyclaw_p8est_new (void);
void             pyclaw_p8est_destroy (pyclaw_p8est_t * pp);

/*** ITERATOR OVER THE FOREST LEAVES ***/

typedef struct pyclaw_p8est_leaf {
  p4est_topidx_t which_tree;
  p4est_locidx_t which_quad;
  p4est_locidx_t total_quad;
  p4est_tree_t * tree;
  p4est_quadrant_t * quad;
  double  lowerleft[3];
  double  upperright[3];
}
pyclaw_p8est_leaf_t;

/* Create an iterator over the leaves in the forest.
 * Returns a newly allocated state containing the first leaf,
 * or NULL if the local partition of the tree is empty.
 */
pyclaw_p8est_leaf_t * pyclaw_p8est_leaf_first (pyclaw_p8est_t * pp);

/* Move the forest leaf iterator forward.
 * Returns the state that was input with information for the next leaf,
 * or NULL and deallocates the input if called with the last leaf.
 */
pyclaw_p8est_leaf_t * pyclaw_p8est_leaf_next (pyclaw_p8est_leaf_t * leaf);
