# -*- coding: utf-8 -*-
# Copyright 2019 EDF-CERFACS.
"""
Test for MatrixPlot class.
"""
import os
from mock import patch
import openturns as ot
from othdrplot import MatrixPlot

@patch("matplotlib.pyplot.show")
def test_MatrixPlot(mock_show):
    fname = os.path.join(os.path.dirname(__file__), 'data', 'gauss-mixture.csv')
    sample = ot.Sample.ImportFromCSVFile(fname)
    
    mp = MatrixPlot(sample)
    mp.draw()
    
    ks = ot.KernelSmoothing()
    distribution = ks.build(sample)
    mp = MatrixPlot(sample,distribution)
    mp.draw()
    
    fname = os.path.join(os.path.dirname(__file__), 'data', 'gauss-mixture-3D.csv')
    sample = ot.Sample.ImportFromCSVFile(fname)
    
    mp = MatrixPlot(sample)
    mp.draw()
    
    ks = ot.KernelSmoothing()
    distribution = ks.build(sample)
    mp = MatrixPlot(sample,distribution)
    mp.draw()

    # Check data : TODO
