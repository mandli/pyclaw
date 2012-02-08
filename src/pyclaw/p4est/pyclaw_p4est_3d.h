
#include <p8est_mesh.h>

/*** COMPLETE INTERNAL STATE OF P4EST ***/

typedef struct pyclaw_p8est {
  int            p4est_dim;
  int            p4est_half;
  int            p4est_faces;
  int            p4est_children;
  p8est_connectivity_t * conn;
  p8est_t * p4est;
  p8est_ghost_t * ghost;
  p8est_mesh_t * mesh;
}
pyclaw_p8est_t;

pyclaw_p8est_t * pyclaw_p8est_new (int initial_level);
void             pyclaw_p8est_destroy (pyclaw_p8est_t * pp);

/*** ITERATOR OVER THE FOREST LEAVES ***/

typedef struct pyclaw_p8est_leaf {
  pyclaw_p8est_t * pp;
  int            level;
  p4est_topidx_t which_tree;
  p4est_locidx_t which_quad;
  p4est_locidx_t total_quad;
  p8est_tree_t * tree;
  p8est_quadrant_t * quad;
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