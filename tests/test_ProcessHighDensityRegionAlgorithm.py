# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Test for ProcessHighDensityRegionAlgorithm class.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from mock import patch
from numpy.testing import assert_equal
import openturns as ot
from openturns.viewer import View
from othdrplot import ProcessHighDensityRegionAlgorithm


@patch("matplotlib.pyplot.show")
def test_ProcessHighDensityRegionAlgorithm(mock_show):
    ot.RandomGenerator.SetSeed(0)
    numberOfPointsForSampling = 500
    ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetBySampling', 'true')
    ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetSamplingSize',
                       str(numberOfPointsForSampling))

    # Dataset
    fname = os.path.join(os.path.dirname(__file__), 'data', 'npfda-elnino.dat')
    data = np.loadtxt(fname)

    # Create the mesh
    n_nodes = data.shape[1]
    mesher = ot.IntervalMesher([n_nodes - 1])
    Interval = ot.Interval([0.0], [1.0])
    mesh = mesher.build(Interval)

    # Create the ProcessSample from the data
    n_fields = data.shape[0]
    dim_fields = 1
    sample = ot.ProcessSample(mesh, n_fields, dim_fields)
    for i in range(n_fields):
        trajectory = ot.Sample(data[i, :], 1)
        sample[i] = ot.Field(mesh, trajectory)

    # Compute HDRPlot
    hdr = ProcessHighDensityRegionAlgorithm(sample)
    hdr.setContoursAlpha([0.8, 0.5])
    hdr.setOutlierAlpha(0.8)
    hdr.run()
    hdr.summary()

    # Plot ACP
    fig, axs, graphs = hdr.drawDimensionReduction()
    plt.show()

    # Plot Density
    fig, axs, graphs = hdr.drawDensity()
    plt.show()

    # Plot outlier trajectories
    graph = hdr.drawOutlierTrajectories(drawInliers=True, discreteMean=True)
    View(graph)
    plt.show()

    graph = hdr.drawOutlierTrajectories(bounds=False)
    View(graph)
    plt.show()

    outlier_indices = hdr.computeOutlierIndices()
    expected_outlier_indices = [3, 7, 22, 32, 33, 41, 47]
    assert_equal(outlier_indices, expected_outlier_indices)

    # Check data
    assert_equal(hdr.getNumberOfTrajectories(), 54)
    assert_equal(hdr.getNumberOfVertices(), 12)
    assert_equal(hdr.numberOfComponents, 2)

    # Check higher dimension
    hdr = ProcessHighDensityRegionAlgorithm(sample)
    hdr.setOutlierAlpha(0.6)
    hdr.setThreshold(0.05)
    hdr.run()

    assert_equal(hdr.numberOfComponents, 3)

    fig, axs, graphs = hdr.drawDensity()
    plt.show()

    fig, axs, graphs = hdr.drawDensity(drawData=True)
    plt.show()
