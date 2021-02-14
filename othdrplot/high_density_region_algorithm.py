# -*- coding: utf-8 -*-
# Copyright 2018 - 2021 - EDF-CERFACS.
"""
Component to create HighDensityRegionAlgorithm.
"""
import numpy as np
import openturns as ot


class HighDensityRegionAlgorithm:
    """Compute the Highest Density Region."""

    def __init__(self, sample, distribution, alphaLevels=[0.9, 0.5, 0.1]):
        """
        Compute a High Density Region.

        Parameters
        ----------
        sample : ot.Sample
            The sample.
        distribution : ot.Distribution
            The distribution which fits the sample.
        alphaLevels : list(float)
            The list of alpha levels for minimum volume level set algorithm.
        """

        # Check input
        if len(alphaLevels) == 0:
            raise ValueError("The number of alpha levels is zero.")
        if sample.getDimension() != distribution.getDimension():
            raise ValueError(
                "The dimension of the sample is %d but "
                "the dimension of the distribution is %d."
                % (sample.getDimension(), distribution.getDimension())
            )

        # Number of points per dim to draw the contour
        self.numberOfPointsInXAxis = 30
        self.numberOfPointsInYAxis = 30

        # The list of probabilities to create the contour
        self.alphaLevels = alphaLevels
        self.alphaLevels.sort(reverse=True)
        self.outlierAlpha = float(np.max(self.alphaLevels))

        # Graphical style
        self.data_marker = "fsquare"  # The marker for data
        self.contour_color = "black"
        self.outlier_color = "firebrick3"
        self.inlier_color = "forestgreen"

        self.sample = sample
        self.distribution = distribution
        self.dim = sample.getDimension()

        # Computed by the algorithm
        self.pvalues = None
        self.levelsets = []
        self.outlierPvalue = None
        self.outlier_levelset = None

    def run(self):
        """Compute pvalues and level sets."""
        n_contour_lines = len(self.alphaLevels)
        # Compute the regular level sets
        self.pvalues = np.zeros(n_contour_lines)
        for i in range(n_contour_lines):
            (
                levelset,
                pvalue,
            ) = self.distribution.computeMinimumVolumeLevelSetWithThreshold(
                self.alphaLevels[i]
            )
            self.pvalues[i] = pvalue
            self.levelsets.append(levelset)

        # Compute the outlier level set
        levelset, pvalue = self.distribution.computeMinimumVolumeLevelSetWithThreshold(
            self.outlierAlpha
        )

        self.outlierPvalue = pvalue
        self.outlier_levelset = levelset

        # Compute the modal level set
        pdf = np.array(self.distribution.computePDF(self.sample))
        self.idx_mode = int(np.argmax(pdf))
        
        # Compute inliers and outliers indices
        flag = self.outlier_levelset.contains(self.sample)
        # Compute outliers
        sample_idx = np.where(np.array(flag) == 0)[0]
        self.outlier_indices = [int(i) for i in sample_idx]
        # Compute inliers
        sample_idx = np.where(np.array(flag) != 0)[0]
        self.inlier_indices = [int(i) for i in sample_idx]

    def getMode(self):
        """
        Return indice of point with highest density.

        The mode is the point of the sample which has highest PDF. 

        Returns
        -------
        index : index
            The indice of the mode in the sample.
        """
        return self.idx_mode

    def computeIndices(self, outlierFlag=True):
        """
        Get inlier or outlier indices.

        The outliers are computed based on the lowest values of the density.
        These regions are computed from the minimum volume level sets 
        which correspond to the levels in alphaLevels.
        The threshold is computed from the maximum values in alphaLevels.
        If e.g. this treshold is equal to 0.9, then the outliers are 
        in the region containing less than 1 - 0.9 = 0.1 fraction 
        of the mass of the density. 

        Parameters
        ----------
        outlierFlag : bool
            If False, compute indices of inlier points.
            If True, compute indices of outlier points.

        Returns
        -------
        indices : list(int)
            The indices of selected points in the sample.
        """
        if outlierFlag:
            # Compute outliers
            indices = self.outlier_indices
        else:
            # Compute inliers
            indices = self.inlier_indices
        return indices

    def setnumberOfPointsInXAxis(self, numberOfPointsInXAxis):
        self.numberOfPointsInXAxis = numberOfPointsInXAxis

    def getnumberOfPointsInXAxis(self):
        return self.numberOfPointsInXAxis

    def setnumberOfPointsInYAxis(self, numberOfPointsInYAxis):
        self.numberOfPointsInYAxis = numberOfPointsInYAxis

    def getnumberOfPointsInYAxis(self):
        return self.numberOfPointsInYAxis

    def _inliers_outliers(self, sample, inliers=True):
        """Inliers or outliers cloud drawing."""
        # Perform selection
        if inliers:
            idx = self.inlier_indices
            legend = "Inliers at alpha=%.4f" % (self.outlierAlpha)
            marker_color = self.inlier_color
        else:
            idx = self.outlier_indices
            legend = "Outliers at alpha=%.4f" % (self.outlierAlpha)
            marker_color = self.outlier_color

        sample_selection = sample[idx, :]

        if sample_selection.getSize() == 0:
            return

        cloud = ot.Cloud(sample_selection, marker_color, self.data_marker, legend)
        return cloud

    def _drawInliers(self, sample):
        """Draw inliers."""
        return self._inliers_outliers(sample, inliers=True)

    def _drawOutliers(self, sample):
        """Draw outliers."""
        return self._inliers_outliers(sample, inliers=False)

    def draw(self, drawInliers=False, drawOutliers=True):
        """
        Draw the high density regions.

        Parameters
        ----------
        drawInliers : bool
            If True, draw inliers points.
        drawOutliers : bool
            If True, draw outliers points.
        """
        plabels = self.sample.getDescription()

        # Bivariate space
        grid = ot.GridLayout(self.dim, self.dim)
        # Axis are created and stored top to bottom, left to right
        for i in range(self.dim):
            for j in range(self.dim):
                if i >= j:  # lower triangle
                    graph = ot.Graph("", "", "", True, "topright")

                if i == j:  # diag
                    marginal_distribution = self.distribution.getMarginal(i)
                    curve = marginal_distribution.drawPDF()
                    graph.add(curve)
                    if drawInliers:
                        marginal_sample = self.sample[self.inlier_indices, i]
                        data = ot.Sample(marginal_sample.getSize(), 2)
                        data[:, 0] = marginal_sample
                        cloud = ot.Cloud(data)
                        cloud.setColor(self.inlier_color)
                        graph.add(cloud)
                    if drawOutliers:
                        marginal_sample = self.sample[self.outlier_indices, i]
                        data = ot.Sample(marginal_sample.getSize(), 2)
                        data[:, 0] = marginal_sample
                        cloud = ot.Cloud(data)
                        cloud.setColor(self.outlier_color)
                        graph.add(cloud)

                elif i > j:  # lower corners
                    # Use a regular grid to compute probability response surface
                    X1min = self.sample[:, j].getMin()[0]
                    X1max = self.sample[:, j].getMax()[0]
                    X2min = self.sample[:, i].getMin()[0]
                    X2max = self.sample[:, i].getMax()[0]

                    xx = ot.Box(
                        [self.numberOfPointsInXAxis], ot.Interval([X1min], [X1max])
                    ).generate()

                    yy = ot.Box(
                        [self.numberOfPointsInXAxis], ot.Interval([X2min], [X2max])
                    ).generate()

                    xy = ot.Box(
                        [self.numberOfPointsInXAxis, self.numberOfPointsInXAxis],
                        ot.Interval([X1min, X2min], [X1max, X2max]),
                    ).generate()

                    data = self.distribution.getMarginal([j, i]).computePDF(xy)

                    # Label using percentage instead of probability
                    n_contours = len(self.alphaLevels)
                    labels = [
                        "%.0f %%" % (self.alphaLevels[i] * 100)
                        for i in range(n_contours)
                    ]

                    contour = ot.Contour(
                        xx, yy, data, self.pvalues, ot.Description(labels)
                    )
                    contour.setColor(self.contour_color)

                    graph.add(contour)

                    sample_ij = self.sample[:, [j, i]]

                    if drawInliers:
                        cloud = self._drawInliers(sample_ij)

                        if cloud is not None:
                            graph.add(cloud)

                    if drawOutliers:
                        cloud = self._drawOutliers(sample_ij)
                        if cloud is not None:
                            graph.add(cloud)

                if j == 0 and i > 0:
                    graph.setYTitle(plabels[i])
                if i == self.dim - 1:
                    graph.setXTitle(plabels[j])

                if i >= j:  # lower triangle
                    graph.setLegends([""])
                    grid.setGraph(i, j, graph)

        return grid
    
    def getOutlierAlpha(self):
        """
        Return alpha level of outliers. 

        Returns
        -------
        outlierAlpha : float
            The alpha level of outliers.
        """
        return self.outlierAlpha

    def getOutlierPValue(self):
        """
        Return p-value of outlier level set. 

        Returns
        -------
        outlierPvalue : float
            The p-value of outlier level set.
        """
        return self.outlierPvalue
