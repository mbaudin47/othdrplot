# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Component to create ProcessHighDensityRegionAlgorithm.
"""
import numpy as np
import openturns as ot
from .high_density_region_algorithm import HighDensityRegionAlgorithm


class ProcessHighDensityRegionAlgorithm:
    """ProcessHighDensityRegionAlgorithm."""

    def __init__(self, processSample, numberOfComponents=2):
        """Density draw based on a :attr:`ProcessSample`.

        :param processSample: Process sample.
        :param int numberOfComponents: Number of components to use.
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
        self.numberOfComponents = numberOfComponents
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

    def drawDimensionReduction(self):
        """Pairdraw of the principal components.

        :return: OpenTURNS Graph object.
        :rtype: :class:`openturns.Graph`
        """
        graph = ot.Graph('Reduced Space', '', '', True, 'topright')
        cloud = ot.Pairs(self.principalComponents)
        cloud.setLabels(self.principalComponents.getDescription())
        graph.add(cloud)

        return graph

    def drawDensity(self, drawData=False, drawOutliers=True):
        """Density draw based on HDR.

        If :attr:`drawData`, the whole sample is drawn. Otherwise, depending on
        :attr:`drawOutliers` it will either show the outliers or the inliers
        only.

        :param bool drawData: Plot inliers and outliers.
        :param bool drawOutliers: Whether to draw inliers or outliers.
        :return: HDR in an OpenTURNS graph object.
        :rtype: :class:`openturns.Graph`
        """
        graph = self.densityPlot.drawContour(drawData, drawOutliers)

        return graph

    def drawTrajectories(self, discreteMean=False):
        """Plot trajectories from the :attr:`ProcessSample`.

        :param bool discreteMean: Whether to compute the mean per vertex.
        :return: OpenTURNS graph object.
        :rtype: :class:`openturns.Graph`
        """
        graph = ot.Graph('Trajectories', '', '', True, 'topright')

        mesh = self.processSample.getMesh()
        t = np.array(mesh.getVertices())
        for i in range(self.n_trajectories):
            traj_curves = ot.Curve(t, self.sample[:, i])
            graph.add(traj_curves)

        # Plot central curve
        if discreteMean:
            central_field = self.processSample.computeMean()
        else:
            central_field = self.processSample[self.densityPlot.idx_mode]

        central_curve = ot.Curve(t, central_field.getValues(), 'Central curve')
        central_curve.setColor('black')
        central_curve.setLineWidth(2)
        graph.add(central_curve)

        return graph

    def drawOutlierTrajectories(self, drawInliers=False, discreteMean=False):
        """Plot trajectories with confidence intervals from the :attr:`ProcessSample`.

        :param bool drawInliers: Whether to draw inliers or not.
        :param bool discreteMean: Whether to compute the mean per vertex or
          by minimal volume levelset using the distribution.
        """
        graph = ot.Graph("Outliers at alpha=%.4f" % (self.densityPlot.outlierAlpha),
                         '', '', True, 'topright')

        # Get the mesh
        mesh = self.processSample.getMesh()
        t = np.ravel(mesh.getVertices())

        # Plot outlier trajectories
        outlier_samples = np.array(self.getOutlierSamples())

        if outlier_samples.size != 0:
            for outlier_sample in outlier_samples.T:
                curve = ot.Curve(t, outlier_sample)
                curve.setColor('red')
                graph.add(curve)

        # Plot inlier trajectories
        inlier_samples = np.array(self.getInlierSamples())

        if drawInliers:
            for inlier_sample in inlier_samples.T:
                curve = ot.Curve(t, inlier_sample)
                curve.setColor('blue')
                graph.add(curve)

        # Plot inlier bounds

        def fill_between_(lower, upper, legend):
            """Draw a shaded area between two curves."""
            disc = len(lower)
            palette = ot.Drawable.BuildDefaultPalette(2)[1]
            poly_data = [[lower[i], lower[i + 1], upper[i + 1], upper[i]]
                         for i in range(disc - 1)]

            polygon = [ot.Polygon(poly_data[i], palette, palette)
                       for i in range(disc - 1)]
            bounds_poly = ot.PolygonArray(polygon)
            bounds_poly.setLegend(legend)

            return bounds_poly

        inlier_min = list(zip(t, np.min(inlier_samples, axis=1)))
        inlier_max = list(zip(t, np.max(inlier_samples, axis=1)))

        bounds = fill_between_(inlier_min, inlier_max,
                               "Inlier at alpha=%.4f" % (self.outlierAlpha))
        graph.add(bounds)

        # Plot central curve
        if discreteMean:
            central_field = self.processSample.computeMean()
        else:
            central_field = self.processSample[self.densityPlot.idx_mode]

        curve = ot.Curve(t[:, None], central_field.getValues(), 'Central curve')
        curve.setColor('black')
        graph.add(curve)

        return graph

    def computeOutlierIndices(self):
        indices = self.densityPlot.computeOutlierIndices()
        return indices

    def getInlierSamples(self):
        indices = self.densityPlot.computeOutlierIndices(False)
        inlier_samples = np.array(self.sample)[:, indices]
        return ot.Sample(inlier_samples)

    def getOutlierSamples(self):
        indices = self.densityPlot.computeOutlierIndices()
        outlier_samples = np.array(self.sample)[:, indices]
        return ot.Sample(outlier_samples)

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
