# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Un composant pour créer des ProcessHighDensityRegionAlgorithm.

TODO : identifier la trajectoire de plus forte densité

TODO : proposer une alternative pour la réduction de dimension : Karhunen-Loève

Références : TODO
"""
import numpy as np
import pylab as pl
import openturns as ot
from .high_density_region_algorithm import HighDensityRegionAlgorithm


class ProcessHighDensityRegionAlgorithm:
    def __init__(self, processSample):
        '''
        Create a new DensityPlot based on a ProcessSample and a distribution.
        '''
        self.processSample = processSample
        # Create data from procesSample : each column is a trajectory
        mymesh = processSample.getMesh()
        self.verticesNumber = mymesh.getVerticesNumber()
        self.sample = ot.Sample(self.verticesNumber, self.processSample.getSize())
        numberOfTrajectories = self.processSample.getSize()
        for i in range(numberOfTrajectories):
            thisTrajectory = self.processSample[i]
            self.sample[:, i] = thisTrajectory.getValues()
        # Check dimension
        dim = processSample.getDimension()
        if (dim != 1):
            raise ValueError(
                'The dimension of the process sample must be equal to 1, but current dimension is %d.' % (dim))
        self.principalComponents = None
        self.numberOfComponents = 2
        self.densityPlot = None
        self.densityPlot = None
        # The list of probabilities to create the contour
        self.contoursAlpha = [0.9, 0.5, 0.1]
        self.outlierAlpha = 0.9  # The probability for outlier detection
        self.explained_variance_ratio = None

    def setContoursAlpha(self, contoursAlpha):
        self.contoursAlpha = contoursAlpha

    def setOutlierAlpha(self, outlierAlpha):
        self.outlierAlpha = outlierAlpha

    def run(self):
        self.runPCA()
        self.runKS()

    def runPCA(self):
        # Perform PCA
        data = np.array(self.sample).T
        # Make the column-mean zero
        columnmean = data.mean(axis=0)
        for i in range(self.verticesNumber):
            data[:, i] = data[:, i] - columnmean[i]
        # Compute SVD of the matrix
        mymatrix = ot.Matrix(data)
        singular_values, U, VT = mymatrix.computeSVD(True)
        V = VT.transpose()
        # Truncate
        VL = V[:, 0:self.numberOfComponents]
        # Project
        self.principalComponents = np.array(mymatrix * VL)
        # Compute explained variance
        explained_variance = ot.Point(self.verticesNumber)
        for i in range(self.verticesNumber):
            explained_variance[i] = singular_values[i]**2
        n_samples = self.processSample.getSize()
        explained_variance /= n_samples - 1
        # Compute total variance
        total_var = explained_variance.norm1()
        # Compute explained variance ratio
        explained_variance_ratio = explained_variance / total_var
        # Truncate
        self.explained_variance_ratio = explained_variance_ratio[0:self.numberOfComponents]

    def runKS(self):
        # Create kernel smoothing
        myks = ot.KernelSmoothing()
        principalComponentsSample = ot.Sample(self.principalComponents)
        sampleDistribution = myks.build(principalComponentsSample)
        # Create DensityPlot
        self.densityPlot = HighDensityRegionAlgorithm(
            principalComponentsSample, sampleDistribution)
        self.densityPlot.setContoursAlpha(self.contoursAlpha)
        self.densityPlot.setOutlierAlpha(self.outlierAlpha)
        self.densityPlot.run()

    def summary(self):
        print("Number of trajectories = %d" % (self.processSample.getSize()))
        print("Number of vertices = %d" % (self.verticesNumber))

    def dimensionReductionSummary(self):
        print("Number of components : %d" % (self.numberOfComponents))
        s = np.sum(self.explained_variance_ratio)
        print('Part of variance : %.4f' % (s))
        print('Explained variance ratio : %s'
              % str(self.explained_variance_ratio))

    def plotDimensionReduction(self):
        pl.scatter(self.principalComponents[:, 0], self.principalComponents[:, 1])
        pl.xlabel("PC1")
        pl.ylabel("PC2")
        pl.show()

    def plotDensity(self, plotData, plotOutliers):
        # Draw contour
        self.densityPlot.plotContour(plotData, plotOutliers)
        return None

    def plotTrajectories(self):
        mymesh = self.processSample.getMesh()
        t = np.array(mymesh.getVertices())
        pl.plot(t, self.sample, "b-")
        # Plot mean
        meanField = self.processSample.computeMean()
        pl.plot(t, meanField.getValues(), "k-", label="Mean")
        #
        pl.legend()
        return None

    def plotOutlierTrajectories(self, plotInliner=False):
        # Get the mesh
        mymesh = self.processSample.getMesh()
        t = np.ravel(mymesh.getVertices())
        dataArray = np.array(self.sample)
        # Plot outlier trajectories
        outlierIndices = self.densityPlot.computeOutlierIndices()
        if (outlierIndices != []):
            outlierSample = dataArray[:, outlierIndices]
            pl.plot(t, outlierSample, "r-")
        # Plot inlier trajectories
        inlierIndices = self.densityPlot.computeOutlierIndices(False)
        inlierSample = dataArray[:, inlierIndices]
        if (plotInliner):
            pl.plot(t, inlierSample, "b-")
        # Plot inlier bounds
        inlierMin = np.min(inlierSample, axis=1)
        inlierMax = np.max(inlierSample, axis=1)
        pl.fill_between(t, inlierMin, inlierMax, where=inlierMax >= inlierMin,
                        facecolor='green', label="Inlier at alpha=%.4f" % (self.outlierAlpha))
        # Plot mean
        meanField = self.processSample.computeMean()
        pl.plot(t, meanField.getValues(), "k-", label="Mean")
        # Oups !
        # pl.legend()
        pl.title("Outliers at alpha=%.4f" % (self.densityPlot.outlierAlpha))
        #
        pl.legend()
        return inlierSample

    def computeOutlierIndices(self):
        indices = self.densityPlot.computeOutlierIndices()
        return indices

    def getNumberOfTrajectories(self):
        return self.processSample.getSize()

    def getNumberOfVertices(self):
        return self.verticesNumber

    def getNumberOfComponents(self):
        return self.numberOfComponents

    def getExplainedVarianceRatio(self):
        return self.explained_variance_ratio

    def getPartOfExplainedVariance(self):
        return np.sum(self.explained_variance_ratio)
