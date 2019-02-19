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
    hdrplot = ProcessHighDensityRegionAlgorithm(sample)
    hdrplot.setContoursAlpha([0.8, 0.5])
    hdrplot.setOutlierAlpha(0.8)
    hdrplot.run()
    hdrplot.summary()
    hdrplot.dimensionReductionSummary()

    # Plot ACP
    hdrplot.plotDimensionReduction()
    plt.show()

    # Plot Density
    plotData = True
    plotOutliers = True
    graph = hdrplot.plotDensity(plotData, plotOutliers)
    View(graph)
    plt.show()

    # Plot trajectories
    hdrplot.plotTrajectories()
    plt.show()

    # Plot outlier trajectories
    hdrplot.plotOutlierTrajectories()
    plt.show()

    outlier_indices = hdrplot.computeOutlierIndices()
    expected_outlier_indices = [3, 7, 22, 32, 33, 41, 47]
    assert_equal(outlier_indices, expected_outlier_indices)

    # Check data
    assert_equal(hdrplot.getNumberOfTrajectories(), 54)
    assert_equal(hdrplot.getNumberOfVertices(), 12)
    assert_equal(hdrplot.getNumberOfComponents(), 2)
    assert_array_almost_equal(hdrplot.getPartOfExplainedVariance(), 0.86569783, 4)
    assert_array_almost_equal(hdrplot.getExplainedVarianceRatio(),
                              [0.60759627, 0.25810156], 4)
