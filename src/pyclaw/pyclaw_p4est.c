
/* This file contains general code that does not depend on space dimension */

#include "pyclaw_p4est.h"
#include <p4est_base.h>

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
