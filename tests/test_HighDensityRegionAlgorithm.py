# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Test for ProcessHighDensityRegionAlgorithm class.
"""
import os
import matplotlib.pyplot as plt
from mock import patch
from numpy.testing import assert_equal
import openturns as ot
from openturns.viewer import View
from othdrplot import HighDensityRegionAlgorithm


@patch("matplotlib.pyplot.show")
def test_HighDensityRegionAlgorithm(mock_show):
    ot.RandomGenerator.SetSeed(0)
    numberOfPointsForSampling = 500
    ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetBySampling', 'true')
    ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetSamplingSize',
                       str(numberOfPointsForSampling))

    # Dataset
    fname = os.path.join(os.path.dirname(__file__), 'data', 'gauss-mixture.csv')
    sample = ot.Sample.ImportFromCSVFile(fname)

    # Creation du kernel smoothing
    ks = ot.KernelSmoothing()
    sample_distribution = ks.build(sample)

    dp = HighDensityRegionAlgorithm(sample, sample_distribution)
    dp.run()

    # Draw contour/inliers/outliers
    graph = ot.Graph('High Density Region draw', '', '', True, 'topright')

    graph.add(dp.drawContour())
    View(graph)
    plt.show()

    graph.add(dp.drawInliers())
    View(graph)
    plt.show()

    # Plot data
    graph.add(dp.drawOutliers())
    View(graph)
    plt.show()

    dp.dim = 3
    graph = ot.Graph('High Density Region draw', '', '', True, 'topright')
    graph.add(dp.drawOutliers())
    View(graph)
    plt.show()

    outlierIndices = dp.computeOutlierIndices()
    expected_outlierIndices = [31, 60, 84, 105, 116, 121, 150, 151, 200, 207, 215,
                               218, 220, 248, 282, 284, 291, 359, 361, 378, 382,
                               404, 412, 418, 425, 426, 433, 449, 450, 457, 461,
                               466, 474, 490, 498, 567, 587, 616, 634, 638, 652,
                               665, 687, 714, 729, 730, 748, 751, 794, 876, 894,
                               896, 903, 925, 928, 963, 968, 987]
    assert_equal(outlierIndices, expected_outlierIndices)
