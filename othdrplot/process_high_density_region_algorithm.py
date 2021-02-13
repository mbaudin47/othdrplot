# -*- coding: utf-8 -*-
# Copyright 2018 - 2021 - EDF-CERFACS.
"""
Component to create ProcessHighDensityRegionAlgorithm.
"""
import numpy as np
import openturns as ot
from .high_density_region_algorithm import HighDensityRegionAlgorithm


class ProcessHighDensityRegionAlgorithm(HighDensityRegionAlgorithm):
    """ProcessHighDensityRegionAlgorithm."""

    def __init__(
        self,
        processSample,
        reducedComponents,
        reducedDistribution,
        alphaLevels=[0.5, 0.9],
    ):
        """
        Density draw based on a ProcessSample.

        Parameters
        ----------
        processSample : ot.ProcessSample
            The collection of processes.
        reducedComponents : ot.Sample
            The sample in the reduced space.
        reducedDistribution : ot.Distribution
            The distribution of points in the reduced space.
        alphaLevels : list(float)
            The list of alpha levels for minimum volume level set algorithm.
        """
        # Chek input
        if reducedDistribution.getDimension() != reducedComponents.getDimension():
            raise ValueError(
                "Dimension of distribution = %d does not math dimension of reduced sample = %d"
                % (reducedDistribution.getDimension(), reducedComponents.getDimension())
            )

        # Check dimension
        dim = processSample.getDimension()
        if dim != 1:
            raise ValueError(
                "The dimension of the process sample must be equal to 1, but "
                "current dimension is %d." % (dim)
            )
        self.processSample = processSample

        # Graphical style
        self.central_color = "black"
        self.default_confidence_band_color = "#87cefa"
        # TODO : setting alpha color to 125 produces vertical bands: why?
        self.default_confidence_band_alpha = 255
        color_hex = ot.Drawable.ConvertFromName(self.default_confidence_band_color)
        r, g, b, a = ot.Drawable.ConvertToRGBA(color_hex)
        self.confidence_band_color = ot.Drawable.ConvertFromRGBA(
            r, g, b, self.default_confidence_band_alpha
        )
        super(ProcessHighDensityRegionAlgorithm, self).__init__(reducedComponents, reducedDistribution, alphaLevels)

    def draw(
        self, drawInliers=False, drawOutliers=True, discreteMean=False, bounds=True
    ):
        """
        Plot outlier trajectories based on HDR.

        Parameters
        ----------
        drawInliers : bool
            If True, plots the inlier curves.
        drawOutliers : bool
            If True, draw the outliers curves.
        discreteMean : bool
            If False, the central curve is the curve in the process sample
            which has highest density.
            If True, the central curve is the mean of the process sample.
        bounds : bool
            If True, plots the bounds of the confidence interval.
            These bounds are made of the mininimum and maximum at
            each time.

        Returns
        -------
        graph : ot.Graph
            The plot of outlier trajectories.
        """
        outlierAlpha = self.getOutlierAlpha()
        graph = ot.Graph(
            r"Outliers at $\alpha$=%.2f" % (outlierAlpha),
            "",
            "",
            True,
            "topright",
        )

        # Get the mesh
        mesh = self.processSample.getMesh()
        t = np.ravel(mesh.getVertices())

        # Plot outlier trajectories
        outlier_indices = self.computeIndices()
        if len(outlier_indices) > 0:
            outlier_process_sample = ot.ProcessSample(mesh, len(outlier_indices), 1)
            index = 0
            for i in outlier_indices:
                outlier_process_sample[index] = self.processSample[i]
                index += 1
            if drawOutliers:
                outlier_graph = outlier_process_sample.drawMarginal(0)
                outlier_graph.setColors([self.outlier_color])
                graph.add(outlier_graph)

        # Plot inlier trajectories
        inlier_indices = self.computeIndices(False)
        if len(inlier_indices):
            inlier_process_sample = ot.ProcessSample(mesh, len(inlier_indices), 1)
            index = 0
            for i in inlier_indices:
                inlier_process_sample[index] = self.processSample[i]
                index += 1
            if drawInliers:
                inlier_graph = inlier_process_sample.drawMarginal(0)
                inlier_graph.setColors([self.inlier_color])
                graph.add(inlier_graph)

        # Plot inlier bounds
        def fill_between(lower, upper, legend, color):
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
            inlier_min = inlier_process_sample.computeQuantilePerComponent(0.0)
            inlier_max = inlier_process_sample.computeQuantilePerComponent(1.0)
            min_values = inlier_min.getValues()
            max_values = inlier_max.getValues()
            nbVertices = mesh.getVerticesNumber()
            lower_bound = [[t[i], min_values[i, 0]] for i in range(nbVertices)]
            upper_bound = [[t[i], max_values[i, 0]] for i in range(nbVertices)]

            outlierAlpha = np.max(self.alphaLevels)
            bounds = fill_between(
                lower_bound,
                upper_bound,
                r"Conf. interval at $\alpha$=%.2f" % (outlierAlpha),
                self.confidence_band_color,
            )
            graph.add(bounds)

        # Plot central curve
        if discreteMean:
            central_field = self.processSample.computeMean()
        else:
            mode_index = self.getMode()
            central_field = self.processSample[mode_index]

        curve = ot.Curve(t[:, None], central_field, "Central curve")
        curve.setColor(self.central_color)
        graph.add(curve)

        return graph
