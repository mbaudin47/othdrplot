# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Test de la classe ProcessHighDensityRegionAlgorithm.
"""
import unittest
import pylab as pl
from numpy.testing import assert_equal
import openturns as ot
from othdrplot import HighDensityRegionAlgorithm


class TestProcessHighDensityRegionAlgorithm(unittest.TestCase):
    def test_default(self):
        ot.RandomGenerator.SetSeed(0)
        numberOfPointsForSampling = 500
        ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetBySampling', 'true')
        ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetSamplingSize',
                           str(numberOfPointsForSampling))

        sample = ot.Sample.ImportFromCSVFile('../data/gauss-mixture.csv')

        # Creation du kernel smoothing
        myks = ot.KernelSmoothing()
        sampleDistribution = myks.build(sample)

        mydp = HighDensityRegionAlgorithm(sample, sampleDistribution)

        mydp.run()

        # Draw contour
        plotData = False
        pl.figure()
        mydp.plotContour(plotData)

        # Plot data
        pl.figure()
        mydp.plotContour(True)

        outlierIndices = mydp.computeOutlierIndices()
        expected_outlierIndices = [31, 60, 84, 105, 116, 121, 150, 151, 200, 207, 215,
                                   218, 220, 248, 282, 284, 291, 359, 361, 378, 382,
                                   404, 412, 418, 425, 426, 433, 449, 450, 457, 461,
                                   466, 474, 490, 498, 567, 587, 616, 634, 638, 652,
                                   665, 687, 714, 729, 730, 748, 751, 794, 876, 894,
                                   896, 903, 925, 928, 963, 968, 987]
        assert_equal(outlierIndices, expected_outlierIndices)


if __name__ == '__main__':
    unittest.main()
