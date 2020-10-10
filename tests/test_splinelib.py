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
from context import splinelib
from splinelib import cspline as csp


class TestCubicSpline(unittest.TestCase):
    """Library of tests for the splinelin.py module"""

    def setUp(self):
        """Method executed once before every test."""
        rnd.seed(0)
        self.xvals = [rnd.random() for _ in range(5)]
        self.yvals = [rnd.random() for _ in range(5)]
        self.Mvals = [rnd.random() for _ in range(5)]
        self.test_spline = csp.CubicSpline(self.xvals, self.yvals, self.Mvals)
        print(f"Executing {self._testMethodName}")

    def test_len(self):
        self.assertEqual(len(self.test_spline), 5)

    def test_repr(self):
        self.assertEqual(repr(self.test_spline),
                         f"CubicSpline('{self.xvals}, {self.yvals}, {self.Mvals}')")

    def test_str(self):
        """Writes the spline attributes on file, then reads them, parses the
        contents and compare them with the actual splines attributes."""
        with open('test_print.txt', 'w') as fh:
            print(self.test_spline, file=fh)
        with open('test_print.txt', 'r') as fh:
            contents = fh.readlines()
        # Extract numbers
        search_filter = r"[-+]?\d*\.\d+|\d+"
        len_printed = re.findall(search_filter, contents[0])
        x_printed = re.findall(search_filter, contents[1])
        y_printed = re.findall(search_filter, contents[2])
        M_printed = re.findall(search_filter, contents[3])
        # Check
        xdiff = [np.abs(float(x_printed[i]) - self.test_spline.xlist[i]
                        ) < 1e-4 for i in range(len(self.test_spline))]
        ydiff = [np.abs(float(y_printed[i]) - self.test_spline.ylist[i]
                        ) < 1e-4 for i in range(len(self.test_spline))]
        Mdiff = [np.abs(float(M_printed[i]) - self.test_spline.Mlist[i]
                        ) < 1e-4 for i in range(len(self.test_spline))]
        self.assertEqual(int(len_printed[0]), len(self.test_spline))
        self.assertTrue(all(xdiff))
        self.assertTrue(all(ydiff))
        self.assertTrue(all(Mdiff))
        # Clean-up
        os.remove('test_print.txt')

    def test_dict_form(self):
        test_spline = csp.CubicSpline([1., 2., 3.], [4., 5., 6.], [7., 8., 9.])
        self.assertEqual(test_spline.dict_form, {'xlist': [1., 2., 3.],
                                                 'ylist': [4., 5., 6.],
                                                 'Mlist': [7., 8., 9.]})

    def test_dict_form_setter(self):
        self.test_spline.dict_form = {'xlist': [11., 22., 33.],
                                      'ylist': [44., 55., 66.],
                                      'Mlist': [77., 88., 99.]}
        self.assertEqual(self.test_spline.xlist, [11., 22., 33.])
        self.assertEqual(self.test_spline.ylist, [44., 55., 66.])
        self.assertEqual(self.test_spline.Mlist, [77., 88., 99.])

    def test_eval(self):
        test_x = [0., 1., 3., 4.5, 5.]
        test_y = [2., -1., 0.5, 3., 1.]
        test_M = [0., 1., 3., 0., -1.]
        test_points = [1., 1.5, 1.7, 2.3, 4.6]
        ref_vals = [-1., -1.3125, -1.3395, -0.9805, 2.608]
        # Create the spline
        test_spline = csp.CubicSpline(test_x, test_y, test_M)
        # Do the checks
        for i, point in enumerate(test_points):
            val = test_spline.eval(point)
            self.assertAlmostEqual(val, ref_vals[i], delta=1e-4,
                                   msg=f"Value in {point} should be {ref_vals[i]}, while it is {val}")

    def test_eval_empty(self):
        test_x = []
        test_y = []
        test_M = []
        # Create the spline
        test_spline = csp.CubicSpline(test_x, test_y, test_M)
        # Do the check
        self.assertIsNone(test_spline.eval(1.))

    def test_eval_single_point(self):
        test_x = [1.]
        test_y = [1.]
        test_M = [1.]
        # Create the spline
        test_spline = csp.CubicSpline(test_x, test_y, test_M)
        # Do the check
        self.assertEqual(test_spline.eval(4.9), test_x[0])

    def test_eval_extrapolation_left(self):
        test_x = [0., 1., 3., 4.5, 5.]
        test_y = [2., -1., 0.5, 3., 1.]
        test_M = [0., 1., 3., 0., -1.]
        # Create the spline
        test_spline = csp.CubicSpline(test_x, test_y, test_M)
        # Do the checks
        self.assertIsInstance(test_spline.eval(-0.5), float)

    def test_eval_extrapolation_right(self):
        test_x = [0., 1., 3., 4.5, 5.]
        test_y = [2., -1., 0.5, 3., 1.]
        test_M = [0., 1., 3., 0., -1.]
        # Create the spline
        test_spline = csp.CubicSpline(test_x, test_y, test_M)
        # Do the checks
        self.assertIsInstance(test_spline.eval(6.), float)

    def test_eval_zero_interval(self):
        test_x = [1., 1.]
        test_y = [2., 2.]
        test_M = [3., 3.]
        # Create the spline
        test_spline = csp.CubicSpline(test_x, test_y, test_M)
        # Do the check
        self.assertIsNone(test_spline.eval(5.))

    def test_read(self):
        text = """Cubic spline. Length: 3
        xlist: 1. 1. 1.
        ylist: 2. 2. 2.
        Mlist: 3. 3. 3.
        """
        with open('test_read.txt', 'w') as fh:
            fh.write(text)
        self.test_spline.read('test_read.txt')
        self.assertEqual(self.test_spline.xlist, [1., 1., 1.])
        self.assertEqual(self.test_spline.ylist, [2., 2., 2.])
        self.assertEqual(self.test_spline.Mlist, [3., 3., 3.])

    def test_reset(self):
        self.test_spline.reset()
        self.assertEqual(self.test_spline.xlist, [])
        self.assertEqual(self.test_spline.ylist, [])
        self.assertEqual(self.test_spline.Mlist, [])


if __name__ == '__main__':
    unittest.main()
