#!/usr/bin/env python
# encoding: utf-8
r"""
Test suite for forestclaw
"""


def test_forestclaw_patch():
    """Test the simple extension of the pyclaw.Patch class"""

    patch = Patch(pyclaw.geometry.Dimension(0.0, 1.0, 10))
    patch.block_number = 2
    patch.mpi_rank = 3


if __name__ == '__main__':
    import nose
    nose.main()