# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Test for ProcessHighDensityRegionAlgorithm class.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import unittest
from numpy.testing import assert_equal
import openturns as ot
from openturns.viewer import View
from othdrplot import ProcessHighDensityRegionAlgorithm

def setup_HDRenv():
    '''
    Setup the HDR environnement.
    '''
    ot.RandomGenerator.SetSeed(0)
    numberOfPointsForSampling = 500
    ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetBySampling', 'true')
    ot.ResourceMap.Set('Distribution-MinimumVolumeLevelSetSamplingSize',
                       str(numberOfPointsForSampling))
    return

def readProcessSample(fname):
    '''
    Return a ProcessSample from a text file. 
    Assume the mesh is regular [0,1].
    '''
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
        trajectory = ot.Sample(data[i, :], 1)
        processSample[i] = ot.Field(mesh, trajectory)
    
    return processSample


class CheckHDRAlgo(unittest.TestCase):

    def test_ProcessHDRAlgorithmDefault(self):
        setup_HDRenv()
    
        # Dataset
        fname = os.path.join(os.path.dirname(__file__), 'data', 'npfda-elnino.dat')
        processSample = readProcessSample(fname)
    
        # Compute HDRPlot
        hdr = ProcessHighDensityRegionAlgorithm(processSample)
        hdr.setContoursAlpha([0.8, 0.5])
        hdr.setOutlierAlpha(0.8)
        hdr.run()
        hdr.summary()
    
        # Plot ACP
        fig = hdr.drawDimensionReduction()
    
        # Plot Density
        fig = hdr.drawDensity()
    
        # Plot outlier trajectories
        graph = hdr.drawOutlierTrajectories(drawInliers=True, discreteMean=True)
    
        graph = hdr.drawOutlierTrajectories(bounds=False)
    
        outlier_indices = hdr.computeOutlierIndices()
        expected_outlier_indices = [3, 7, 22, 32, 33, 41, 47]
        assert_equal(outlier_indices, expected_outlier_indices)
    
        # Check data
        assert_equal(hdr.getNumberOfTrajectories(), 54)
        assert_equal(hdr.getNumberOfVertices(), 12)
        assert_equal(hdr.numberOfComponents, 2)
    
    def test_ProcessHDRAlgorithmThreshold(self):
        setup_HDRenv()
    
        # Dataset
        fname = os.path.join(os.path.dirname(__file__), 'data', 'npfda-elnino.dat')
        processSample = readProcessSample(fname)

        # Customize the dimension reduction
        threshold = 0.05
        algo = ot.KarhunenLoeveSVDAlgorithm(processSample,threshold)
        algo.run()
        karhunenLoeveResult = algo.getResult()
        
        # Check higher dimension
        hdr = ProcessHighDensityRegionAlgorithm(processSample, karhunenLoeveResult)
        hdr.setOutlierAlpha(0.6)
        hdr.run()
        hdr.summary()
    
        assert_equal(hdr.numberOfComponents, 3)
    
        fig = hdr.drawDensity()
    
        fig = hdr.drawDensity(drawData=True)

        # Plot outlier trajectories
        graph = hdr.drawOutlierTrajectories(drawInliers=True, discreteMean=True)

        graph = hdr.drawOutlierTrajectories(bounds=False)

if __name__=="__main__":
    unittest.main()
