"""Created on: 2020-09-30
@author: Giorgio Tosti Balducci

Classes and functions for cubic splines determination."""

# Standard library inputs
import sys
from typing import (List, Tuple)
from random import seed, random

# Third-party imports
import numpy as np

# Local applications imports


class CubicSpline(object):
    """Docstring"""

    def __init__(self, xlist: np.array, ylist: np.array, Mlist: np.array,
                 verbose: bool = False):
        """Characterization of the cubic spline:
        Args:
            xlist: knots
            ylist: interpolated values
            Mlist: 2nd derivatives at the knots"""
        self.xlist = xlist
        self.ylist = ylist
        self.Mlist = Mlist

        # Debugging print
        if verbose:
            print(self)

    def __len__(self):
        """Returns the length of the cubic spline."""
        return len(self.xlist)

    def __repr__(self):
        """Returns a representation of the spline object. Used for re-creating
        the object."""
        return f"CubicSpline('{self.xlist}, {self.ylist}, {self.Mlist}')"

    def __str__(self):
        """Returns a readable representation of the spline. Used for printing.
        """
        xout = "xlist: "
        yout = "ylist: "
        Mout = "Mlist: "
        for i in range(len(self)):
            xout += "%10.3f" % (self.xlist[i])
            yout += "%10.3f" % (self.ylist[i])
            Mout += "%10.3f" % (self.Mlist[i])
        return f"""Cubic spline. Length: %4d
        {xout}
        {yout}
        {Mout}""" % (len(self))


if __name__ == '__main__':
    seed(0)
    xvals = [random() for _ in range(5)]
    yvals = [random() for _ in range(5)]
    Mvals = [random() for _ in range(5)]
    myspline = CubicSpline(xvals, yvals, Mvals)
    print(repr(myspline))
    print(myspline)
