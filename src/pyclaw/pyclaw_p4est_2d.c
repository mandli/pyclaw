
#ifndef P4_TO_P8
#include "pyclaw_p4est_2d.h"
#include <p4est_bits.h>
#include <p4est_extended.h>
#else
#include "pyclaw_p4est_3d.h"
#include <p8est_bits.h>
#include <p8est_extended.h>
#endif

pyclaw_p4est_t *
pyclaw_p4est_new (void)
{
  pyclaw_p4est_t * pp;

  pp = SC_ALLOC (pyclaw_p4est_t, 1);
  pp->p4est_dim = P4EST_DIM;
  pp->p4est_half = P4EST_HALF;
  pp->p4est_faces = P4EST_FACES;
  pp->p4est_children = P4EST_CHILDREN;
#ifndef P4_TO_P8
  pp->conn = p4est_connectivity_new_unitsquare ();
#else
  pp->conn = p8est_connectivity_new_unitcube ();
#endif
  pp->p4est = p4est_new_ext (MPI_COMM_WORLD, pp->conn,
			     0, 1, 1, 0, NULL, NULL);
  pp->ghost = p4est_ghost_new (pp->p4est, P4EST_CONNECT_FULL);
  pp->mesh = p4est_mesh_new (pp->p4est, pp->ghost, P4EST_CONNECT_FULL);

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

static pyclaw_p4est_leaf_t *
pyclaw_p4est_leaf_info (pyclaw_p4est_leaf_t * leaf) {
#ifdef P4EST_DEBUG
  int		   nface;
  p4est_mesh_t    *mesh = leaf->pp->mesh;
#endif
  p4est_quadrant_t corner;

  leaf->total_quad = leaf->tree->quadrants_offset + leaf->which_quad;
  leaf->quad = p4est_quadrant_array_index (&leaf->tree->quadrants,
					   leaf->which_quad);

  leaf->level = (int) leaf->quad->level;
  p4est_qcoord_to_vertex (leaf->pp->conn, leaf->which_tree,
			  leaf->quad->x, leaf->quad->y,
#ifdef P4_TO_P8
			  leaf->quad->z,
#endif
			  leaf->lowerleft);
  p4est_quadrant_corner_node (leaf->quad, P4EST_CHILDREN - 1, &corner);
  p4est_qcoord_to_vertex (leaf->pp->conn, leaf->which_tree,
			  corner.x, corner.y,
#ifdef P4_TO_P8
			  corner.z,
#endif
			  leaf->upperright);

#ifdef P4EST_DEBUG
  printf ("C: Leaf level %d tree %d tree_leaf %d local_leaf %d\n",
	  leaf->level, leaf->which_tree, leaf->which_quad, leaf->total_quad);
  for (nface = 0; nface < P4EST_FACES; ++nface) {
    printf ("C: Leaf face %d leaf %d\n", nface,
	    mesh->quad_to_quad[P4EST_FACES * leaf->total_quad + nface]);
  }
#endif

  return leaf;
}

pyclaw_p4est_leaf_t *
pyclaw_p4est_leaf_first (pyclaw_p4est_t * pp)
{
  pyclaw_p4est_leaf_t * leaf;
  p4est_t * p4est = pp->p4est;

  if (p4est->local_num_quadrants == 0) {
    return NULL;
  }

  leaf = SC_ALLOC (pyclaw_p4est_leaf_t, 1);
  leaf->pp = pp;
  leaf->which_tree = p4est->first_local_tree;
  leaf->tree = p4est_tree_array_index (p4est->trees, leaf->which_tree);
  P4EST_ASSERT (leaf->tree->quadrants.elem_size > 0);
  leaf->which_quad = 0;

  return pyclaw_p4est_leaf_info (leaf);
}

pyclaw_p4est_leaf_t *
pyclaw_p4est_leaf_next (pyclaw_p4est_leaf_t * leaf)
{
  p4est_t * p4est = leaf->pp->p4est;

  P4EST_ASSERT (leaf != NULL);

  if ((size_t) leaf->which_quad + 1 == leaf->tree->quadrants.elem_count) {
    ++leaf->which_tree;
    if (leaf->which_tree > p4est->last_local_tree) {
      SC_FREE (leaf);
      return NULL;
    }
    leaf->tree = p4est_tree_array_index (p4est->trees, leaf->which_tree);
    P4EST_ASSERT (leaf->tree->quadrants.elem_size > 0);
    leaf->which_quad = 0;
  }
  else {
    ++leaf->which_quad;
  }

  return pyclaw_p4est_leaf_info (leaf);
}
