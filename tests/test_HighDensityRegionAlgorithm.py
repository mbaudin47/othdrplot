# -*- coding: utf-8 -*-
# Copyright 2018 - 2019 EDF-CERFACS.
"""
Test for ProcessHighDensityRegionAlgorithm class.
"""
import os
from numpy.testing import assert_equal
import openturns as ot
import othdrplot as othdr
import unittest
import othdrplot
import openturns.viewer as otv


class CheckHDRAlgo(unittest.TestCase):
    def test_HighDensityRegionAlgorithm2D(self):
        # With 2D
        ot.RandomGenerator.SetSeed(0)
        numberOfPointsForSampling = 500
        ot.ResourceMap.SetAsBool("Distribution-MinimumVolumeLevelSetBySampling", True)
        ot.ResourceMap.Set(
            "Distribution-MinimumVolumeLevelSetSamplingSize",
            str(numberOfPointsForSampling),
        )

        # Dataset
        fname = os.path.join(othdrplot.__path__[0], "data", "gauss-mixture.csv")
        sample = ot.Sample.ImportFromCSVFile(fname)

        # Creation du kernel smoothing
        ks = ot.KernelSmoothing()
        distribution = ks.build(sample)

        dp = othdr.HighDensityRegionAlgorithm(sample, distribution)
        dp.run()

        # Draw contour/inliers/outliers
        otv.View(dp.draw())

        otv.View(dp.draw(drawInliers=True))

        otv.View(dp.draw(drawOutliers=False))

        outlierIndices = dp.computeIndices()
        expected_outlierIndices = [
            31,
            60,
            84,
            105,
            116,
            121,
            150,
            151,
            200,
            207,
            215,
            218,
            220,
            248,
            282,
            284,
            291,
            359,
            361,
            378,
            382,
            404,
            412,
            418,
            425,
            426,
            433,
            449,
            450,
            457,
            461,
            466,
            474,
            490,
            498,
            567,
            587,
            616,
            634,
            638,
            652,
            665,
            687,
            714,
            729,
            730,
            748,
            751,
            794,
            876,
            894,
            896,
            903,
            925,
            928,
            963,
            968,
            987,
        ]
        assert_equal(outlierIndices, expected_outlierIndices)
        # Mode
        mode_index = dp.getMode()
        assert_equal(mode_index, 424)

    def test_HighDensityRegionAlgorithm3D(self):
        # With 3D
        ot.RandomGenerator.SetSeed(0)
        numberOfPointsForSampling = 500
        ot.ResourceMap.SetAsBool("Distribution-MinimumVolumeLevelSetBySampling", True)
        ot.ResourceMap.Set(
            "Distribution-MinimumVolumeLevelSetSamplingSize",
            str(numberOfPointsForSampling),
        )

        # Dataset
        fname = os.path.join(othdrplot.__path__[0], "data", "gauss-mixture-3D.csv")
        sample = ot.Sample.ImportFromCSVFile(fname)

        # Creation du kernel smoothing
        ks = ot.KernelSmoothing()
        distribution = ks.build(sample)

        dp = othdr.HighDensityRegionAlgorithm(sample, distribution, [0.8, 0.3])
        dp.run()

        # Draw contour/inliers/outliers
        otv.View(dp.draw())
        otv.View(dp.draw(drawInliers=True))
        otv.View(dp.draw(drawOutliers=False))

        outlierIndices = dp.computeIndices()
        expected_outlierIndices = [
            75,
            79,
            145,
            148,
            189,
            246,
            299,
            314,
            340,
            351,
            386,
            471,
        ]
        assert_equal(outlierIndices, expected_outlierIndices)

    def test_HighDensityRegionAlgorithm1D(self):
        # With 1D
        ot.RandomGenerator.SetSeed(0)
        numberOfPointsForSampling = 500
        ot.ResourceMap.SetAsBool("Distribution-MinimumVolumeLevelSetBySampling", True)
        ot.ResourceMap.Set(
            "Distribution-MinimumVolumeLevelSetSamplingSize",
            str(numberOfPointsForSampling),
        )

        # Dataset
        ot.RandomGenerator_SetSeed(1976)
        sample = ot.Normal().getSample(100)

        # Creation du kernel smoothing
        ks = ot.KernelSmoothing()
        distribution = ks.build(sample)

        dp = othdr.HighDensityRegionAlgorithm(sample, distribution)
        dp.run()

        # Draw contour/inliers/outliers
        otv.View(dp.draw())

        otv.View(dp.draw(drawInliers=True))

        otv.View(dp.draw(drawOutliers=False))

        outlierIndices = dp.computeIndices()
        expected_outlierIndices = [16, 24, 33, 49, 71, 84]
        assert_equal(outlierIndices, expected_outlierIndices)


if __name__ == "__main__":
    unittest.main()
