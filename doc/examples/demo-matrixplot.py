# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:44:28 2019

@author: c61372
"""

import os
import openturns as ot
from othdrplot import MatrixPlot

fname = os.path.join('Z:/Activites2019/VIGIE-HDRPlot-2019/othdrplot/tests/data/gauss-mixture.csv')
sample = ot.Sample.ImportFromCSVFile(fname)

mp = MatrixPlot(sample)
mp.draw()

ks = ot.KernelSmoothing()
distribution = ks.build(sample)
mp = MatrixPlot(sample,distribution)
mp.draw()

fname = os.path.join('Z:/Activites2019/VIGIE-HDRPlot-2019/othdrplot/tests/data/gauss-mixture-3D.csv')
sample = ot.Sample.ImportFromCSVFile(fname)

mp = MatrixPlot(sample)
mp.draw()

ks = ot.KernelSmoothing()
distribution = ks.build(sample)
mp = MatrixPlot(sample,distribution)
mp.draw()
