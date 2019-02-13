# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Test de la classe ProcessHighDensityRegionAlgorithm.
"""
import unittest
import numpy as np
import pylab as pl
from numpy.testing import assert_equal, assert_array_almost_equal
import openturns as ot
from othdrplot import ProcessHighDensityRegionAlgorithm


class TestProcessHighDensityRegionAlgorithm(unittest.TestCase):
    def test_default(self):
        ot.RandomGenerator.SetSeed(0)
        numberOfPointsForSampling = 500
        ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetBySampling', 'true')
        ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetSamplingSize',
                           str(numberOfPointsForSampling))
        #
        dataR = np.loadtxt('../data/npfda-elnino.dat')

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
        pl.figure()
        myhdrplot.plotDimensionReduction()

        # Plot Density
        pl.figure()
        plotData = True
        plotOutliers = True
        myhdrplot.plotDensity(plotData, plotOutliers)

        # Plot trajectories
        pl.figure()
        myhdrplot.plotTrajectories()

        # Plot outlier trajectories
        pl.figure()
        myhdrplot.plotOutlierTrajectories()

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


if __name__ == '__main__':
    unittest.main()
