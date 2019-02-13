# -*- coding: utf-8 -*-
# Copyright 2018 EDF.

import numpy as np
import openturns as ot
import pylab as pl
import ProcessHighDensityRegionAlgorithm as hdrplot

# Configure OT
numberOfPointsForSampling=500
ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetBySampling', 'true')
ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetSamplingSize', str(numberOfPointsForSampling))

# https://www.math.univ-toulouse.fr/~ferraty/SOFTWARES/NPFDA/npfda-datasets.html
dataR = np.loadtxt('../data/npfda-elnino.dat')

# Create the mesh
numberOfNodes = dataR.shape[1]
myMesher = ot.IntervalMesher([numberOfNodes-1])
myInterval = ot.Interval([0.0], [1.0])
myMesh = myMesher.build(myInterval)
myMesh.draw()

# Create the ProcessSample from the data
numberOfFields = dataR.shape[0]
dimensionOfFields = 1
myps = ot.ProcessSample(myMesh, numberOfFields, dimensionOfFields)
for i in range(numberOfFields):
    thisTrajectory = ot.Sample(dataR[i,:],1)
    myps[i] = ot.Field(myMesh,thisTrajectory)

# Compute HDRPlot
myhdrplot = hdrplot.ProcessHighDensityRegionAlgorithm(myps)
myhdrplot.setContoursAlpha([0.8,0.5])
myhdrplot.setOutlierAlpha(0.8)
myhdrplot.run()
myhdrplot.summary()
myhdrplot.dimensionReductionSummary()

# Plot ACP
pl.figure()
myhdrplot.plotDimensionReduction()

# Plot Density
pl.figure()
plotData = True
plotOutliers = True
myhdrplot.plotDensity(plotData,plotOutliers)

# Plot trajectories
pl.figure()
myhdrplot.plotTrajectories()

# Plot outlier trajectories
pl.figure()
inlierSample = myhdrplot.plotOutlierTrajectories()

print("Outliers trajectories at alpha=%.4f" % (myhdrplot.densityPlot.outlierAlpha))
outlierIndices = myhdrplot.computeOutlierIndices()
print(outlierIndices)
