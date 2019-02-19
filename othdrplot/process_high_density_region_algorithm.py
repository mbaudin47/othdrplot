# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Component to create ProcessHighDensityRegionAlgorithm.
"""
import numpy as np
import matplotlib.pyplot as plt
import openturns as ot
from .high_density_region_algorithm import HighDensityRegionAlgorithm


class ProcessHighDensityRegionAlgorithm:
    """ProcessHighDensityRegionAlgorithm."""

    def __init__(self, processSample):
        """Density plot based on a :attr:`ProcessSample`.

        :param processSample: Process sample.
        :type processSample: :class:`openturns.ProcessSample`
        """
        self.processSample = processSample

        # Create data from processSample : each column is a trajectory
        mesh = processSample.getMesh()
        self.verticesNumber = mesh.getVerticesNumber()
        self.sample = ot.Sample(self.verticesNumber, self.processSample.getSize())
        self.n_trajectories = self.processSample.getSize()

        for i in range(self.n_trajectories):
            trajectory = self.processSample[i]
            self.sample[:, i] = trajectory.getValues()

        # Check dimension
        dim = processSample.getDimension()
        if dim != 1:
            raise ValueError(
                'The dimension of the process sample must be equal to 1, but '
                'current dimension is %d.' % (dim))
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
        """Sequencially run PCA and KS."""
        self.runPCA()
        self.runKS()

    def runPCA(self):
        """Perform PCA."""
        data = np.array(self.sample).T
        # Make the column-mean zero
        columnmean = data.mean(axis=0)
        for i in range(self.verticesNumber):
            data[:, i] = data[:, i] - columnmean[i]

        # Compute SVD of the matrix
        matrix = ot.Matrix(data)
        singular_values, U, VT = matrix.computeSVD(True)
        V = VT.transpose()

        # Truncate
        VL = V[:, 0:self.numberOfComponents]
        # Project
        self.principalComponents = ot.Sample(np.array(matrix * VL))
        labels = ['PC' + str(i) for i in range(self.numberOfComponents)]
        self.principalComponents.setDescription(labels)

        # Compute explained variance
        explained_variance = ot.Point(self.verticesNumber)
        for i in range(self.verticesNumber):
            explained_variance[i] = singular_values[i] ** 2

        n_samples = self.processSample.getSize()
        explained_variance /= n_samples - 1
        # Compute total variance
        total_var = explained_variance.norm1()
        # Compute explained variance ratio
        explained_variance_ratio = explained_variance / total_var
        # Truncate
        self.explained_variance_ratio = explained_variance_ratio[0:self.numberOfComponents]

    def runKS(self):
        """Create kernel smoothing."""
        ks = ot.KernelSmoothing()
        sample_distribution = ks.build(self.principalComponents)
        # Create DensityPlot
        self.densityPlot = HighDensityRegionAlgorithm(
            self.principalComponents, sample_distribution)
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
        """Pairplot of the principal components.

        :return: OpenTURNS Graph object.
        :rtype: :class:`openturns.Graph`
        """
        graph = ot.Graph('Reduced Space', '', '', True, 'topright')
        cloud = ot.Pairs(self.principalComponents)
        cloud.setLabels(self.principalComponents.getDescription())
        graph.add(cloud)

        return graph

    def plotDensity(self, plotData=False, plotOutliers=True):
        """Density plot based on HDR.

        If :attr:`plotData`, the whole sample is drawn. Otherwise, depending on
        :attr:`plotOutliers` it will either show the outliers or the inliers
        only.

        :param bool plotData: Plot inliers and outliers.
        :param bool plotOutliers: Whether to plot inliers or outliers.
        :return: HDR in an OpenTURNS graph object.
        :rtype: :class:`openturns.Graph`
        """
        graph = self.densityPlot.plotContour(plotData, plotOutliers)

        return graph

    def plotTrajectories(self):
        """Plot trajectories from the :attr:`ProcessSample`.

        :return: OpenTURNS graph object.
        :rtype: :class:`openturns.Graph`
        """
        graph = ot.Graph('Trajectories', '', '', True, 'topright')

        mesh = self.processSample.getMesh()
        t = np.array(mesh.getVertices())
        for i in range(self.n_trajectories):
            traj_curves = ot.Curve(t, self.sample[:, i])
            graph.add(traj_curves)

        # Plot mean
        mean_field = self.processSample.computeMean()
        mean_curve = ot.Curve(t, mean_field.getValues(), 'Discrete mean')
        mean_curve.setColor('black')
        mean_curve.setLineWidth(2)
        graph.add(mean_curve)

        return graph

    def plotOutlierTrajectories(self, plotInliner=False):
        """Plot trajectories with confidence intervals from the :attr:`ProcessSample`."""
        # Get the mesh
        mesh = self.processSample.getMesh()
        t = np.ravel(mesh.getVertices())
        dataArray = np.array(self.sample)
        # Plot outlier trajectories
        outlierIndices = self.densityPlot.computeOutlierIndices()

        fig, ax = plt.subplots()

        if outlierIndices.size != 0:
            outlierSample = dataArray[:, outlierIndices]
            ax.plot(t, outlierSample, "r-")

        # Plot inlier trajectories
        inlierIndices = self.densityPlot.computeOutlierIndices(False)
        inlierSample = dataArray[:, inlierIndices]

        if plotInliner:
            ax.plot(t, inlierSample, "b-")

        # Plot inlier bounds
        inlierMin = np.min(inlierSample, axis=1)
        inlierMax = np.max(inlierSample, axis=1)
        ax.fill_between(t, inlierMin, inlierMax, where=inlierMax >= inlierMin,
                        facecolor='green', label="Inlier at alpha=%.4f" % (self.outlierAlpha))
        # Plot mean
        meanField = self.processSample.computeMean()
        ax.plot(t, meanField.getValues(), "k-", label="Mean")
        ax.set_title("Outliers at alpha=%.4f" % (self.densityPlot.outlierAlpha))
        ax.legend()

        return inlierSample, fig, ax

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
