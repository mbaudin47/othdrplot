#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Demonstration de Kernel Smoothing 2D avec OpenTURNS.
Etant donné α dans (0,1), on recherche p dans (0,1) tel que 

P(X dans A(p)) = α 

où 

A(p)={X dans Rn tel que f(x) > p}.

Etant donné α, on cherche le seuil p tel que 
la probabilité d'avoir une densité de points 
supérieure à p est égal à α.


Pour OpenTURNS v1.8
Michael Baudin, 2017
"""

import openturns as ot
import pylab as pl
import HighDensityRegionAlgorithm as dp

# Configure OT
numberOfPointsForSampling=500
ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetBySampling', 'true')
ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetSamplingSize', str(numberOfPointsForSampling))

sample = ot.Sample.ImportFromCSVFile('../data/gauss-mixture.csv')

# Creation du kernel smoothing
myks = ot.KernelSmoothing()
sampleDistribution = myks.build(sample)

mydp = dp.HighDensityRegionAlgorithm(sample,sampleDistribution)

mydp.run()

'''
Default :
Ncontour=30
relativeFactor = 0.1
alpha=[0.9,0.5,0.1]
'''

# 4.. Draw contour
plotData = False
pl.figure()
mydp.plotContour(plotData)

# Plot data
pl.figure()
mydp.plotContour(True)

print("Outliers at alpha=%.4f" % (mydp.outlierAlpha))
outlierIndices = mydp.computeOutlierIndices()
print(outlierIndices)

