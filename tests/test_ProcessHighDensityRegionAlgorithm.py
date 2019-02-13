# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Test for ProcessHighDensityRegionAlgorithm class.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from mock import patch
from numpy.testing import assert_equal, assert_array_almost_equal
import openturns as ot
from othdrplot import ProcessHighDensityRegionAlgorithm


@patch("matplotlib.pyplot.show")
def test_ProcessHighDensityRegionAlgorithm(mock_show):
    ot.RandomGenerator.SetSeed(0)
    numberOfPointsForSampling = 500
    ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetBySampling', 'true')
    ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetSamplingSize',
                       str(numberOfPointsForSampling))
    #
    fname = os.path.join(os.path.dirname(__file__), 'data', 'npfda-elnino.dat')
    dataR = np.loadtxt(fname)

    # Create the mesh
    numberOfNodes = dataR.shape[1]
    myMesher = ot.IntervalMesher([numberOfNodes - 1])
    myInterval = ot.Interval([0.0], [1.0])
    myMesh = myMesher.build(myInterval)

    # Create the ProcessSample from the data
    numberOfFields = dataR.shape[0]
    dimensionOfFields = 1
    myps = ot.ProcessSample(myMesh, numberOfFields, dimensionOfFields)
    for i in range(numberOfFields):
        thisTrajectory = ot.Sample(dataR[i, :], 1)
        myps[i] = ot.Field(myMesh, thisTrajectory)

    # Compute HDRPlot
    myhdrplot = ProcessHighDensityRegionAlgorithm(myps)
    myhdrplot.setContoursAlpha([0.8, 0.5])
    myhdrplot.setOutlierAlpha(0.8)
    myhdrplot.run()
    myhdrplot.summary()
    myhdrplot.dimensionReductionSummary()

    # Plot ACP
    myhdrplot.plotDimensionReduction()
    plt.show()

    # Plot Density
    plotData = True
    plotOutliers = True
    myhdrplot.plotDensity(plotData, plotOutliers)
    plt.show()

    # Plot trajectories
    myhdrplot.plotTrajectories()
    plt.show()

    # Plot outlier trajectories
    myhdrplot.plotOutlierTrajectories()
    plt.show()

    outlierIndices = myhdrplot.computeOutlierIndices()
    expected_outlierIndices = [3, 7, 22, 32, 33, 41, 47]
    assert_equal(outlierIndices, expected_outlierIndices)

    # Check data
    assert_equal(myhdrplot.getNumberOfTrajectories(), 54)
    assert_equal(myhdrplot.getNumberOfVertices(), 12)
    assert_equal(myhdrplot.getNumberOfComponents(), 2)
    assert_array_almost_equal(myhdrplot.getPartOfExplainedVariance(), 0.86569783, 4)
    assert_array_almost_equal(myhdrplot.getExplainedVarianceRatio(), [
                              0.60759627, 0.25810156], 4)
