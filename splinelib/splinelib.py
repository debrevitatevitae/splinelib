"""Created on: 2020-09-30
@author: Giorgio Tosti Balducci

Classes and functions for cubic splines determination."""

# Standard library inputs
from typing import (List, Tuple)

# Third-party imports
import numpy as np

# Local applications imports


class CubicSpline(object):
    """Docstring"""

    def __init__(self, xlist: np.array, ylist: np.array, Mlist: np.array):
        """Data for characterizing the cubic spline:
            xlist: knots
            ylist: interpolated values
            Mlist: 2nd derivatives at the knots"""
        self.xlist = xlist
        self.ylist = xlist
        self.Mlist = xlist
