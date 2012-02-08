PYCLAWMAKE = $(PYCLAW)/Makefile.common
P4ESTMAKE = $(PYCLAW)/src/pyclaw/p4est/Makefile.p4est

RP_SOURCE =   $(RIEMANN)/src/rpn2_acoustics.f90 $(RIEMANN)/src/rpt2_acoustics.f90

all: 
	make classic2.so
	make sharpclaw2.so
	make -f $(P4ESTMAKE)

include $(PYCLAWMAKE)

