"""Created on: 2020-09-30
@author: Giorgio Tosti Balducci

Classes and functions for cubic splines determination."""

# Standard library inputs
import os
from random import seed, random
import re
import sys
from typing import (List, Tuple)

# Third-party imports
import numpy as np

# Local applications imports


class CubicSpline(object):
    """Cubic spline data structure and functions."""

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
        """Return the length of the cubic spline."""
        return len(self.xlist)

    def __repr__(self):
        """Return a representation of the spline object. Used for re-creating
        the object."""
        return f"CubicSpline('{self.xlist}, {self.ylist}, {self.Mlist}')"

    def __str__(self):
        """Return a readable representation of the spline. Used for printing.

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
        """Return a dict representation of the spline."""
        return {'xlist': self.xlist,
                'ylist': self.ylist,
                'Mlist': self.Mlist}

    @dict_form.setter
    def dict_form(self, spline_dict: dict):
        """Set the spline by setting its dict representation."""
        self.xlist = spline_dict['xlist']
        self.ylist = spline_dict['ylist']
        self.Mlist = spline_dict['Mlist']

    @staticmethod
    def _log_spline(iflag, msg, log_file=None):
        fh = open(log_file, 'a') if log_file else sys.stdout
        if iflag == -1:
            print("CubicSpline Error: " + msg, file=fh)
        if iflag == 1:
            print("CubicSpline Warning: " + msg, file=fh)
        if fh != sys.stdout:
            fh.close()

    def eval(self, t: float, log_file=None):
        """Evaluates the cubic spline in t.

        Arguments:
            -- t: evaluation point.
            -- log_file (optional): file where possible errors/warnings are
                logged."""
        # Check on spline's data
        if len(self) == 0:
            iflag = -1
            msg = "No data defined for this spline."
            CubicSpline._log_spline(iflag, msg, log_file=log_file)
            return None
        elif len(self) == 1:
            iflag = 1
            msg = "Only one data point defined. Return te value at that point."
            CubicSpline._log_spline(iflag, msg, log_file=log_file)
            return self.ylist[0]

        # Define initial interval
        lo = 0
        hi = len(self) - 1

        # Check if there will be extrapolation
        if t < self.xlist[0]:
            i = 0
            iflag = 1
            msg = f"Evaluation point t = {t} is lower than x0 = {self.xlist[0]}. Extrapolating."
            CubicSpline._log_spline(iflag, msg, log_file=log_file)
        if t > self.xlist[-1]:
            i = len(self) - 2
            iflag = 1
            msg = f"Evaluation point t = {t} is greater than xn = {self.xlist[-1]}. Extrapolating."
            CubicSpline._log_spline(iflag, msg, log_file=log_file)
        else:
            iflag = 0
            # Binary search of the index
            while hi > lo + 1:
                mid = (lo + hi) // 2  # integer division
                if t < self.xlist[mid]:
                    hi = mid
                else:
                    lo = mid
            i = lo

        # Definition of the interval
        xi = self.xlist[i]
        xii = self.xlist[i + 1]
        h = xii - xi
        if h < 2 * np.finfo(float).eps:  # check if h is less than 2 * eps_mach
            iflag = -1
            msg = "Length of h is zero. Check the spline data."
            CubicSpline._log_spline(iflag, msg, log_file=log_file)
            return None

        # Evaluation in t
        yi = self.ylist[i]
        yii = self.ylist[i + 1]
        Mi = self.Mlist[i]
        Mii = self.Mlist[i + 1]
        diff1 = t - xi
        diff2 = xii - t
        val = diff1 * (yii / h - Mii * h / 6. + diff1 * diff1 * Mii /
                       (6. * h)) + diff2 * (yi / h - Mi * h / 6. + diff2 *
                                            diff2 * Mi / (6. * h))

        return val

    def read(self, filename):
        """Read the spline data from file.

        Assumptions:
            -- The file is written as that printed with __str__"""
        with open(filename, 'r') as fh:
            contents = fh.readlines()
        # Extract numbers
        search_filter = r"[-+]?\d*\.\d+|\d+"
        self.xlist = [float(i) for i in re.findall(search_filter, contents[1])]
        self.ylist = [float(i) for i in re.findall(search_filter, contents[2])]
        self.Mlist = [float(i) for i in re.findall(search_filter, contents[3])]

    def reset(self):
        """Reset all the attributes of the spline instance."""
        self.xlist = []
        self.ylist = []
        self.Mlist = []


if __name__ == '__main__':
    # seed(0)
    # xvals = [random() for _ in range(5)]
    # yvals = [random() for _ in range(5)]
    # Mvals = [random() for _ in range(5)]
    xvals = [0., 1., 3., 4.5, 5.]
    yvals = [2., -1., 0.5, 3., 1.]
    Mvals = [0., 1., 3., 0., -1.]
    myspline = CubicSpline(xvals, yvals, Mvals)
    myspline.eval(4.6)

    # print(repr(myspline))
    # print("Before modifying the spline.")
    # print(myspline)
    # with open("dummy.txt", 'w') as fh:
    #     print(myspline, file=fh)
    # myspline.dict_form = {
    #     'xlist': [1.],
    #     'ylist': [1.],
    #     'Mlist': [1.]
    # }
    # print("After modifying the spline.")
    # print(myspline)
    # myspline.read("dummy.txt")
    # print("After reading the original spline file.")
    # print(myspline)
    # os.remove('dummy.txt')
    #
    # print(myspline.dict_form)
    #
    # mydict = {
    #     'xlist': [1., 2., 3.],
    #     'ylist': [1.1, 2.2, 3.3],
    #     'Mlist': [0., 0., 0.]
    # }
    #
    # myspline.dict_form = mydict
    # print(myspline)
    # myspline.reset()
    # print(myspline.dict_form)
