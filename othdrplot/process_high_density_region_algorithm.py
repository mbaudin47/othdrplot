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

    def __init__(self, processSample, karhunenLoeveResult=None):
        """Density draw based on a :attr:`ProcessSample`.

        :param processSample: Process sample.
        :type processSample: :class:`openturns.ProcessSample`
        """
        self.processSample = processSample

        # Create data from processSample : each column is a trajectory
        mesh = processSample.getMesh()
        self.verticesNumber = mesh.getVerticesNumber()
        self.sample = ot.Sample(self.verticesNumber, self.processSample.getSize())
        self.n_trajectories = self.processSample.getSize()

        # Create the KLresult, if not provided
        if karhunenLoeveResult is None:
            threshold = 0.1  # TODO : set the ResourceMap default setting
            algo = ot.KarhunenLoeveSVDAlgorithm(processSample, threshold)
            algo.run()
            self.karhunenLoeveResult = algo.getResult()
        else:
            self.karhunenLoeveResult = karhunenLoeveResult

        for i in range(self.n_trajectories):
            trajectory = self.processSample[i]
            self.sample[:, i] = trajectory

        # Check dimension
        dim = processSample.getDimension()
        if dim != 1:
            raise ValueError(
                "The dimension of the process sample must be equal to 1, but "
                "current dimension is %d." % (dim)
            )
        self.principalComponents = None
        self.densityPlot = None
        self.densityPlot = None
        # The list of probabilities to create the contour
        self.contoursAlpha = [0.9, 0.5, 0.1]
        self.outlierAlpha = 0.9  # The probability for outlier detection
        self.threshold = 0.1

        # Graphical style
        self.outlier_color = "firebrick3"
        self.inlier_color = "forestgreen"
        self.central_color = "black"
        self.default_confidence_band_color = "#87cefa"
        self.default_confidence_band_alpha = 255
        color_hex = ot.Drawable.ConvertFromName(self.default_confidence_band_color)
        r, g, b, a = ot.Drawable.ConvertToRGBA(color_hex)
        self.confidence_band_color = ot.Drawable.ConvertFromRGBA(
            r, g, b, self.default_confidence_band_alpha
        )

    def setContoursAlpha(self, contoursAlpha):
        self.contoursAlpha = contoursAlpha

    def setOutlierAlpha(self, outlierAlpha):
        self.outlierAlpha = outlierAlpha

    def run(self, distribution=None):
        """Sequencially run DimensionReduction and HDR.

        :param KarhunenLoeveResult: Result structure of a Karhunen Loeve
          algorithm.
        :param distribution: Probability Density Function of the sample.
        :type KarhunenLoeveResult: :class:`openturns.KarhunenLoeveResult`
        :type distribution: :class:`openturns.Distribution`
        """
        self.runDimensionReduction()
        self.runHDR(distribution)

    def runDimensionReduction(self):
        """Perform dimension reduction.

        :param KarhunenLoeveResult: Result structure of a Karhunen Loeve
          algorithm.
        :type KarhunenLoeveResult: :class:`openturns.KarhunenLoeveResult`
        """

        # Project
        self.principalComponents = self.karhunenLoeveResult.project(self.processSample)
        self.numberOfComponents = self.principalComponents.getDimension()
        labels = ["PC" + str(i) for i in range(self.numberOfComponents)]
        self.principalComponents.setDescription(labels)

    def runHDR(self, distribution=None):
        """Create HDR.

        :param distribution: Probability Density Function of the sample.
        :type distribution: :class:`openturns.Distribution`
        """
        if distribution is None:
            ks = ot.KernelSmoothing()
            distribution = ks.build(self.principalComponents)

        # Create DensityPlot
        self.densityPlot = HighDensityRegionAlgorithm(
            self.principalComponents, distribution
        )
        self.densityPlot.setContoursAlpha(self.contoursAlpha)
        self.densityPlot.setOutlierAlpha(self.outlierAlpha)

        self.densityPlot.run()

    def summary(self):
        print("Number of trajectories = %d" % (self.processSample.getSize()))
        print("Number of vertices = %d" % (self.verticesNumber))
        print("Number of components = %d" % (self.numberOfComponents))
        threshold = self.karhunenLoeveResult.getThreshold()
        print("Eigenvalue threshold = %s" % (threshold))

    def drawDimensionReduction(self):
        """Pairdraw of the principal components.

        :returns: figure, axes and OpenTURNS Graph object.
        :rtypes: Matplotlib figure instances, Matplotlib AxesSubplot instances,
          :class:`openturns.Graph`
        """
        dimension = self.principalComponents.getDimension()
        distribution = ot.ComposedDistribution(
            [
                ot.KernelSmoothing().build(self.principalComponents.getMarginal(i))
                for i in range(dimension)
            ]
        )
        if dimension == 1:
            graph = distribution.drawPDF()
            # Add points on X axis
            sample_size = self.principalComponents.getSize()
            data = ot.Sample(sample_size, 2)
            data[:, 0] = self.principalComponents
            cloud = ot.Cloud(data)
            graph.add(cloud)
        else:
            graph = ot.VisualTest_DrawPairsMarginals(
                self.principalComponents, distribution
            )
        return graph

    def drawDensity(self, drawInliers=False, drawOutliers=True):
        """Draw contour.

        If :attr:`drawData`, the whole sample is drawn. Otherwise, depending on
        :attr:`drawOutliers` it will either show the outliers or the inliers
        only.

        :param bool drawData: Plot inliers and outliers.
        :param bool drawOutliers: Whether to draw inliers or outliers.
        :returns: figure, axes and OpenTURNS Graph object.
        :rtypes: Matplotlib figure instances, Matplotlib AxesSubplot instances,
          :class:`openturns.Graph`
        """
        return self.densityPlot.draw(drawInliers=drawInliers, drawOutliers=drawOutliers)

    def drawOutlierTrajectories(
        self, drawInliers=False, discreteMean=False, bounds=True
    ):
        """Plot outlier trajectories from the :attr:`ProcessSample`.

        :param bool drawInliers: Whether to draw inliers or not.
        :param bool discreteMean: Whether to compute the mean per vertex or
          by minimal volume levelset using the distribution.
        :param bool bounds: Whether to plot bounds.
        :return: OpenTURNS graph object.
        :rtype: :class:`openturns.Graph`
        """
        graph = ot.Graph(
            "Outliers at alpha=%.2f" % (self.densityPlot.outlierAlpha),
            "",
            "",
            True,
            "topright",
        )

        # Get the mesh
        mesh = self.processSample.getMesh()
        t = np.ravel(mesh.getVertices())

        # Plot outlier trajectories
        outlier_samples = np.array(self.getOutlierSamples())

        if outlier_samples.size != 0:
            for outlier_sample in outlier_samples.T:
                curve = ot.Curve(t, outlier_sample)
                curve.setColor(self.outlier_color)
                graph.add(curve)

        # Plot inlier trajectories
        inlier_samples = np.array(self.getInlierSamples())

        if drawInliers:
            for inlier_sample in inlier_samples.T:
                curve = ot.Curve(t, inlier_sample)
                curve.setColor(self.inlier_color)
                graph.add(curve)

        # Plot inlier bounds

        def fill_between_(lower, upper, legend, color):
            """Draw a shaded area between two curves."""
            disc = len(lower)
            poly_data = [
                [lower[i], lower[i + 1], upper[i + 1], upper[i]]
                for i in range(disc - 1)
            ]

            polygon = [ot.Polygon(poly_data[i], color, color) for i in range(disc - 1)]
            bounds_poly = ot.PolygonArray(polygon)
            bounds_poly.setLegend(legend)

            return bounds_poly

        if bounds:
            inlier_min = list(zip(t, np.min(inlier_samples, axis=1)))
            inlier_max = list(zip(t, np.max(inlier_samples, axis=1)))

            bounds = fill_between_(
                inlier_min,
                inlier_max,
                "Confidence interval at alpha=%.2f" % (self.outlierAlpha),
                self.confidence_band_color,
            )
            graph.add(bounds)

        # Plot central curve
        if discreteMean:
            central_field = self.processSample.computeMean()
        else:
            central_field = self.processSample[self.densityPlot.idx_mode]

        curve = ot.Curve(t[:, None], central_field, "Central curve")
        curve.setColor(self.central_color)
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
