# -*- coding: utf-8 -*-
# Copyright 2018-2019 EDF-CERFACS.
"""
Test for ProcessHighDensityRegionAlgorithm class.
"""
import os
from numpy.testing import assert_equal
import openturns as ot
from othdrplot import HighDensityRegionAlgorithm
import unittest

class CheckHDRAlgo(unittest.TestCase):

    def test_HighDensityRegionAlgorithm2D(self):
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
        graph = ot.Graph('Test High Density Region plot', '', '', True, 'topright')
    
        fig = dp.drawContour()
    
        fig = dp.drawContour(drawData=True)
    
        fig = dp.drawContour(drawOutliers=False)
    
        graph.add(dp.drawInliers())
    
        # Plot data
        graph.add(dp.drawOutliers())
    
        outlierIndices = dp.computeOutlierIndices()
        expected_outlierIndices = [31, 60, 84, 105, 116, 121, 150, 151, 200, 207, 215,
                                   218, 220, 248, 282, 284, 291, 359, 361, 378, 382,
                                   404, 412, 418, 425, 426, 433, 449, 450, 457, 461,
                                   466, 474, 490, 498, 567, 587, 616, 634, 638, 652,
                                   665, 687, 714, 729, 730, 748, 751, 794, 876, 894,
                                   896, 903, 925, 928, 963, 968, 987]
        assert_equal(outlierIndices, expected_outlierIndices)

    def test_HighDensityRegionAlgorithm3D(self):
        ot.RandomGenerator.SetSeed(0)
        numberOfPointsForSampling = 500
        ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetBySampling', 'true')
        ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetSamplingSize',
                           str(numberOfPointsForSampling))
    
        # Dataset
        fname = os.path.join(os.path.dirname(__file__), 'data', 'gauss-mixture-3D.csv')
        sample = ot.Sample.ImportFromCSVFile(fname)
    
        # Creation du kernel smoothing
        ks = ot.KernelSmoothing()
        sample_distribution = ks.build(sample)
    
        dp = HighDensityRegionAlgorithm(sample, sample_distribution)
        dp.setOutlierAlpha(0.8)
        dp.run()
    
        # Draw contour/inliers/outliers
        graph = ot.Graph('Test High Density Region plot', '', '', True, 'topright')
    
        fig = dp.drawContour()
    
        fig = dp.drawContour(drawData=True)
    
        fig = dp.drawContour(drawOutliers=False)
    
        graph.add(dp.drawInliers())
    
        # Plot data
        graph.add(dp.drawOutliers())
    
        outlierIndices = dp.computeOutlierIndices()
        expected_outlierIndices = [75, 79, 145, 148, 189, 246, 299, 314, 340, 351, 386, 471]
        assert_equal(outlierIndices, expected_outlierIndices)

if __name__=="__main__":
    unittest.main()
