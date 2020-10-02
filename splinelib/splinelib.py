"""Created on: 2020-09-30
@author: Giorgio Tosti Balducci

Classes and functions for cubic splines determination."""

# Standard library inputs
from typing import (List, Tuple)
from random import seed, random

# Third-party imports
import numpy as np

# Local applications imports


class CubicSpline(object):
    """Docstring"""

    def __init__(self, xlist: np.array, ylist: np.array, Mlist: np.array,
                 verbose: bool = False):
        """Data for characterizing the cubic spline:
            xlist: knots
            ylist: interpolated values
            Mlist: 2nd derivatives at the knots"""
        self.xlist = xlist
        self.ylist = ylist
        self.Mlist = Mlist

        # Debugging print
        if verbose:
            print("Created CubicSpline instance. Length = %4d" % (len(self)))
            xout = "xlist: "
            yout = "ylist: "
            Mout = "Mlist: "
            for i in range(len(self)):
                xout += "%10.3f" % (xlist[i])
                yout += "%10.3f" % (ylist[i])
                Mout += "%10.3f" % (Mlist[i])
            print(xout)
            print(yout)
            print(Mout)

    def __len__(self):
        return len(self.xlist)


# if __name__ == '__main__':
#     seed(0)
#     xvals = [random() for _ in range(5)]
#     yvals = [random() for _ in range(5)]
#     Mvals = [random() for _ in range(5)]
#     myspline = CubicSpline(xvals, yvals, Mvals, verbose=True)
