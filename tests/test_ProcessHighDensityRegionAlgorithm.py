# -*- coding: utf-8 -*-
# Copyright 2018 - 2021 EDF - CERFACS.
"""
Test for ProcessHighDensityRegionAlgorithm class.
"""
import os
import numpy as np
import unittest
from numpy.testing import assert_equal
import openturns as ot
import othdrplot as othdr
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


class CheckProcessHDRAlgo(unittest.TestCase):
    def test_ProcessHDRAlgorithmDefault(self):
        # With 2 principal components
        setup_HDRenv()

        # Dataset
        fname = os.path.join(othdr.__path__[0], "data", "npfda-elnino.dat")
        processSample = readProcessSample(fname)

        # KL decomposition
        reduction = othdr.KarhunenLoeveDimensionReductionAlgorithm(processSample, 2)
        reduction.run()
        reducedComponents = reduction.getReducedComponents()

        # Distribution fit in reduced space
        ks = ot.KernelSmoothing()
        reducedDistribution = ks.build(reducedComponents)

        # Compute HDRPlot
        hdr = othdr.ProcessHighDensityRegionAlgorithm(
            processSample, reducedComponents, reducedDistribution, [0.8, 0.5]
        )
        hdr.run()

        # Plot outlier trajectories
        graph = hdr.draw(drawInliers=True, discreteMean=True)
        otv.View(graph)

        graph = hdr.draw(bounds=False)
        otv.View(graph)

        outlier_indices = hdr.computeIndices()
        expected_outlier_indices = [3, 7, 22, 32, 33, 41, 47]
        assert_equal(outlier_indices, expected_outlier_indices)
        return

    def test_ProcessHDRAlgorithmThreshold(self):
        # With 3 principal components
        setup_HDRenv()

        # Dataset
        fname = os.path.join(othdr.__path__[0], "data", "npfda-elnino.dat")
        processSample = readProcessSample(fname)

        # KL decomposition
        reduction = othdr.KarhunenLoeveDimensionReductionAlgorithm(processSample, 3)
        reduction.run()
        reducedComponents = reduction.getReducedComponents()

        # Distribution fit in reduced space
        ks = ot.KernelSmoothing()
        reducedDistribution = ks.build(reducedComponents)

        # Check higher dimension
        hdr = othdr.ProcessHighDensityRegionAlgorithm(
            processSample, reducedComponents, reducedDistribution, [0.6, 0.1]
        )
        hdr.run()

        # Plot outlier trajectories
        graph = hdr.draw(drawInliers=True, discreteMean=True)
        otv.View(graph)

        graph = hdr.draw(bounds=False)
        otv.View(graph)
        return

    def test_ProcessHDRAlgorithmPC1(self):
        # With 1 principal component
        setup_HDRenv()

        # Dataset
        fname = os.path.join(othdr.__path__[0], "data", "npfda-elnino.dat")
        processSample = readProcessSample(fname)

        # Customize the dimension reduction
        reduction = othdr.KarhunenLoeveDimensionReductionAlgorithm(processSample, 1)
        reduction.run()
        reducedComponents = reduction.getReducedComponents()

        # Distribution fit in reduced space
        ks = ot.KernelSmoothing()
        reducedDistribution = ks.build(reducedComponents)

        # Check higher dimension
        hdr = othdr.ProcessHighDensityRegionAlgorithm(
            processSample, reducedComponents, reducedDistribution, [0.1, 0.6]
        )
        hdr.run()

        # Plot outlier trajectories
        graph = hdr.draw(drawInliers=True, discreteMean=True)
        otv.View(graph)

        graph = hdr.draw(bounds=False)
        otv.View(graph)
        return


if __name__ == "__main__":
    unittest.main()
