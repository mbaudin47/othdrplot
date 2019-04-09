# -*- coding: utf-8 -*-
# Copyright 2019 EDF-CERFACS.
"""
Test for MatrixPlot class.
"""
import os
import unittest
import matplotlib.pyplot as plt
import openturns as ot
from othdrplot import MatrixPlot


class CheckHDRAlgo(unittest.TestCase):

    def test_MatrixPlot2D(self):
        fname = os.path.join(os.path.dirname(__file__), 'data', 'gauss-mixture.csv')
        sample = ot.Sample.ImportFromCSVFile(fname)
    
        mp = MatrixPlot(sample)
        fig, axs, graphs = mp.draw()
        plt.show()
    
        ks = ot.KernelSmoothing()
        distribution = ks.build(sample)
        mp = MatrixPlot(sample, distribution)
        fig, axs, graphs = mp.draw()
        plt.show()
    
    def test_MatrixPlot3D(self):
        fname = os.path.join(os.path.dirname(__file__), 'data', 'gauss-mixture-3D.csv')
        sample = ot.Sample.ImportFromCSVFile(fname)
    
        mp = MatrixPlot(sample)
        fig, axs, graphs = mp.draw()
        plt.show()
    
        ks = ot.KernelSmoothing()
        distribution = ks.build(sample)
        mp = MatrixPlot(sample, distribution)
        fig, axs, graphs = mp.draw()
        plt.show()

if __name__=="__main__":
    unittest.main()
