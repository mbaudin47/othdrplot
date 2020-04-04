# -*- coding: utf-8 -*-
# Copyright 2019 EDF-CERFACS.
"""
Test for MatrixPlot class.
"""
import os
import unittest
import openturns as ot
from othdrplot import MatrixPlot


class CheckHDRAlgo(unittest.TestCase):

    def test_MatrixPlot2D(self):
        fname = os.path.join(os.path.dirname(__file__), '..', 'data',
                             'gauss-mixture.csv')
        sample = ot.Sample.ImportFromCSVFile(fname)

        mp = MatrixPlot(sample)
        fig = mp.draw()

        ks = ot.KernelSmoothing()
        distribution = ks.build(sample)
        mp = MatrixPlot(sample, distribution)
        fig = mp.draw()

    def test_MatrixPlot3D(self):
        fname = os.path.join(os.path.dirname(__file__), '..',
                             'data', 'gauss-mixture-3D.csv')
        sample = ot.Sample.ImportFromCSVFile(fname)

        mp = MatrixPlot(sample)
        fig = mp.draw()

        ks = ot.KernelSmoothing()
        distribution = ks.build(sample)
        mp = MatrixPlot(sample, distribution)
        fig = mp.draw()

if __name__ == "__main__":
    unittest.main()
