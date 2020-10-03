"""Created on: 2020-10-03
@author: Giorgio Tosti Balducci

Automated tests for splinelib.py."""

# Standard library inputs
import os
import random as rnd
import re
import sys
import unittest

# Third-party imports
import numpy as np

# Local applications imports
from splinelib import CubicSpline

print(sys.path)


class TestCubicSpline(unittest.TestCase):
    """Library of tests for the splinelin.py module"""

    def setUp(self):
        """Method executed once before every test."""
        rnd.seed(0)
        self.xvals = [rnd.random() for _ in range(5)]
        self.yvals = [rnd.random() for _ in range(5)]
        self.Mvals = [rnd.random() for _ in range(5)]
        self.myspline = CubicSpline(self.xvals, self.yvals, self.Mvals)
        print(f"Executing {self._testMethodName}")

    def test_len(self):
        self.assertEqual(len(self.myspline), 5)

    def test_repr(self):
        self.assertEqual(repr(self.myspline),
                         f"CubicSpline('{self.xvals}, {self.yvals}, {self.Mvals}')")

    def test_str(self):
        """Writes the spline attributes on file, then reads them, parses the
        contents and compare them with the actual splines attributes."""
        with open('test_print.txt', 'w') as fh:
            print(self.myspline, file=fh)
        with open('test_print.txt', 'r') as fh:
            contents = fh.readlines()
        # Extract numbers
        search_filter = r"[-+]?\d*\.\d+|\d+"
        len_printed = re.findall(search_filter, contents[0])
        x_printed = re.findall(search_filter, contents[1])
        y_printed = re.findall(search_filter, contents[2])
        M_printed = re.findall(search_filter, contents[3])
        # Check
        xdiff = [np.abs(float(x_printed[i]) - self.myspline.xlist[i]
                        ) < 1e-4 for i in range(len(self.myspline))]
        ydiff = [np.abs(float(y_printed[i]) - self.myspline.ylist[i]
                        ) < 1e-4 for i in range(len(self.myspline))]
        Mdiff = [np.abs(float(M_printed[i]) - self.myspline.Mlist[i]
                        ) < 1e-4 for i in range(len(self.myspline))]
        self.assertEqual(int(len_printed[0]), len(self.myspline))
        self.assertTrue(all(xdiff))
        self.assertTrue(all(ydiff))
        self.assertTrue(all(Mdiff))
        # Clean-up
        os.remove('test_print.txt')


if __name__ == '__main__':
    unittest.main()
