/*
  This file is part of p4est.
  p4est is a C library to manage a collection (a forest) of multiple
  connected adaptive quadtrees or octrees in parallel.

  Copyright (C) 2012 Carsten Burstedde

  p4est is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  p4est is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with p4est; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
*/

#include <p4est_to_p8est.h>

#define pyclaw_p4est_t          pyclaw_p8est_t
#define pyclaw_p4est_new	pyclaw_p8est_new
#define pyclaw_p4est_destroy	pyclaw_p8est_destroy

#define pyclaw_p4est_leaf_t	pyclaw_p8est_leaf_t
#define pyclaw_p4est_leaf_next	pyclaw_p8est_leaf_next
#define pyclaw_p4est_leaf_first	pyclaw_p8est_leaf_first

#include "pyclaw_p4est_2d.c"
