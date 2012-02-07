
#include <p4est_mesh.h>

/*** COMPLETE INTERNAL STATE OF P4EST ***/

typedef struct pyclaw_p4est {
  p4est_connectivity_t * conn;
  p4est_t * p4est;
  p4est_ghost_t * ghost;
  p4est_mesh_t * mesh;
  int test_number;
}
pyclaw_p4est_t;

pyclaw_p4est_t * pyclaw_p4est_new (void);
void             pyclaw_p4est_destroy (pyclaw_p4est_t * pp);

/*** ITERATOR OVER THE FOREST LEAVES ***/

typedef struct pyclaw_p4est_leaf {
  pyclaw_p4est_t * pp;
  p4est_topidx_t which_tree;
  p4est_locidx_t which_quad;
  p4est_locidx_t total_quad;
  p4est_tree_t * tree;
  p4est_quadrant_t * quad;
  double  lowerleft[3];
  double  upperright[3];
}
pyclaw_p4est_leaf_t;

/* Create an iterator over the leaves in the forest.
 * Returns a newly allocated state containing the first leaf,
 * or NULL if the local partition of the tree is empty.
 */
pyclaw_p4est_leaf_t * pyclaw_p4est_leaf_first (pyclaw_p4est_t * pp);

/* Move the forest leaf iterator forward.
 * Returns the state that was input with information for the next leaf,
 * or NULL and deallocates the input if called with the last leaf.
 */
pyclaw_p4est_leaf_t * pyclaw_p4est_leaf_next (pyclaw_p4est_leaf_t * leaf);
