# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Test for ProcessHighDensityRegionAlgorithm class.
"""
import os
import numpy as np
import unittest
from numpy.testing import assert_equal
import openturns as ot
from othdrplot import ProcessHighDensityRegionAlgorithm
import othdrplot
import openturns.viewer as otv


def setup_HDRenv():
    """
    Setup the HDR environnement.
    """
    ot.RandomGenerator.SetSeed(0)
    numberOfPointsForSampling = 500
    ot.ResourceMap.SetAsBool("Distribution-MinimumVolumeLevelSetBySampling", True)
    ot.ResourceMap.Set(
        "Distribution-MinimumVolumeLevelSetSamplingSize", str(numberOfPointsForSampling)
    )
    return


def readProcessSample(fname):
    """
    Return a ProcessSample from a text file.
    Assume the mesh is regular [0,1].
    """
    # Dataset
    data = np.loadtxt(fname)

    # Create the mesh
    n_nodes = data.shape[1]
    mesher = ot.IntervalMesher([n_nodes - 1])
    Interval = ot.Interval([0.0], [1.0])
    mesh = mesher.build(Interval)

    # Create the ProcessSample from the data
    n_fields = data.shape[0]
    dim_fields = 1
    processSample = ot.ProcessSample(mesh, n_fields, dim_fields)
    for i in range(n_fields):
        trajectory = ot.Sample([[x] for x in data[i, :]])
        processSample[i] = ot.Field(mesh, trajectory)
    return processSample


class CheckHDRAlgo(unittest.TestCase):
    def test_ProcessHDRAlgorithmDefault(self):
        # With 2 principal components
        setup_HDRenv()

        # Dataset
        fname = os.path.join(othdrplot.__path__[0], "data", "npfda-elnino.dat")
        processSample = readProcessSample(fname)

        # Compute HDRPlot
        hdr = ProcessHighDensityRegionAlgorithm(processSample)
        hdr.setContoursAlpha([0.8, 0.5])
        hdr.setOutlierAlpha(0.8)
        hdr.run()
        hdr.summary()

        # Plot ACP
        grid = hdr.drawDimensionReduction()
        otv.View(grid)

        # Plot Density
        grid = hdr.drawDensity()
        otv.View(grid)

        # Plot outlier trajectories
        graph = hdr.drawOutlierTrajectories(drawInliers=True, discreteMean=True)
        otv.View(graph)

        graph = hdr.drawOutlierTrajectories(bounds=False)
        otv.View(graph)

        outlier_indices = hdr.computeOutlierIndices()
        expected_outlier_indices = [3, 7, 22, 32, 33, 41, 47]
        assert_equal(outlier_indices, expected_outlier_indices)

        # Check data
        assert_equal(hdr.getNumberOfTrajectories(), 54)
        assert_equal(hdr.getNumberOfVertices(), 12)
        assert_equal(hdr.numberOfComponents, 2)
        return

    def test_ProcessHDRAlgorithmThreshold(self):
        # With 3 principal components
        setup_HDRenv()

        # Dataset
        fname = os.path.join(othdrplot.__path__[0], "data", "npfda-elnino.dat")
        processSample = readProcessSample(fname)

        # Customize the dimension reduction
        threshold = 0.05
        algo = ot.KarhunenLoeveSVDAlgorithm(processSample, threshold)
        algo.run()
        karhunenLoeveResult = algo.getResult()

        # Check higher dimension
        hdr = ProcessHighDensityRegionAlgorithm(processSample, karhunenLoeveResult)
        hdr.setOutlierAlpha(0.6)
        hdr.run()
        hdr.summary()

        assert_equal(hdr.numberOfComponents, 3)

        grid = hdr.drawDensity()
        otv.View(grid)

        grid = hdr.drawDensity(drawInliers=True)
        otv.View(grid)

        # Plot outlier trajectories
        graph = hdr.drawOutlierTrajectories(drawInliers=True, discreteMean=True)
        otv.View(graph)

        graph = hdr.drawOutlierTrajectories(bounds=False)
        otv.View(graph)

        # Plot principal components
        grid = hdr.drawDimensionReduction()
        otv.View(grid)
        return

    def test_ProcessHDRAlgorithmPC1(self):
        # With 1 principal component
        setup_HDRenv()

        # Dataset
        fname = os.path.join(othdrplot.__path__[0], "data", "npfda-elnino.dat")
        processSample = readProcessSample(fname)

        # Customize the dimension reduction
        threshold = 0.5
        algo = ot.KarhunenLoeveSVDAlgorithm(processSample, threshold)
        algo.setNbModes(1)
        algo.run()
        karhunenLoeveResult = algo.getResult()

        # Check higher dimension
        hdr = ProcessHighDensityRegionAlgorithm(processSample, karhunenLoeveResult)
        hdr.setOutlierAlpha(0.6)
        hdr.run()
        hdr.summary()

        assert_equal(hdr.numberOfComponents, 1)

        grid = hdr.drawDensity()
        otv.View(grid)

        grid = hdr.drawDensity(drawInliers=True)
        otv.View(grid)

        # Plot outlier trajectories
        graph = hdr.drawOutlierTrajectories(drawInliers=True, discreteMean=True)
        otv.View(graph)

        graph = hdr.drawOutlierTrajectories(bounds=False)
        otv.View(graph)

        # Plot principal components
        grid = hdr.drawDimensionReduction()
        otv.View(grid)
        return


if __name__ == "__main__":
    unittest.main()
