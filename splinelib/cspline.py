"""Created on: 2020-09-30
@author: Giorgio Tosti Balducci

Classes and functions for cubic splines determination."""

# Standard library inputs
from random import seed, random
from typing import (List, Tuple)

# Third-party imports
import numpy as np

# Local applications imports


class CubicSpline(object):
    """Docstring"""

    def __init__(self, xlist: List, ylist: List, Mlist: List,
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

        Assumptions:
            -- xlist, ylist an Mlist all have the same length.
        """
        xout = "xlist: "
        yout = "ylist: "
        Mout = "Mlist: "
        for i in range(len(self)):
            xout += "%10.5f" % (self.xlist[i])
            yout += "%10.5f" % (self.ylist[i])
            Mout += "%10.5f" % (self.Mlist[i])
        return f"""Cubic spline. Length: %4d
        {xout}
        {yout}
        {Mout}""" % (len(self))

    @property
    def dict_form(self):
        """Returns a dict representation of the spline."""
        return {'xlist': self.xlist,
                'ylist': self.ylist,
                'Mlist': self.Mlist}

    @dict_form.setter
    def dict_form(self, spline_dict):
        """Sets the spline by setting its dict representation."""
        self.xlist = spline_dict['xlist']
        self.ylist = spline_dict['ylist']
        self.Mlist = spline_dict['Mlist']

    def reset(self):
        """Resets all the attributes of the spline instance."""
        self.xlist = []
        self.ylist = []
        self.Mlist = []


if __name__ == '__main__':
    seed(0)
    xvals = [random() for _ in range(5)]
    yvals = [random() for _ in range(5)]
    Mvals = [random() for _ in range(5)]
    myspline = CubicSpline(xvals, yvals, Mvals)
    print(repr(myspline))
    print(myspline)

    print(myspline.dict_form)

    mydict = {
        'xlist': [1., 2., 3.],
        'ylist': [1.1, 2.2, 3.3],
        'Mlist': [0., 0., 0.]
    }

    myspline.dict_form = mydict
    print(myspline)
    myspline.reset()
    print(myspline.dict_form)
