# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Component to create HighDensityRegionAlgorithm.
"""
import numpy as np
import matplotlib.pyplot as plt
import openturns as ot
import openturns.viewer as otv


class HighDensityRegionAlgorithm:
    """Compute the Highest Density Region."""

    def __init__(self, sample, distribution):
        """Compute a High Density Region.

        :param sample: Sample of size (n_samples, n_dims).
        :param distribution: Probability Density Function of the sample.
        :type sample: :class:`openturns.Sample`
        :type distribution: :class:`openturns.Distribution`
        """
        # Number of points per dim to draw the contour
        self.numberOfPointsInXAxis = 30
        self.numberOfPointsInYAxis = 30

        # The list of probabilities to create the contour
        self.contoursAlpha = [0.9, 0.5, 0.1]
        self.outlierAlpha = 0.9  # The probability for outlier detection

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
        n_contour_lines = len(self.contoursAlpha)
        # Compute the regular level sets
        self.pvalues = np.zeros(n_contour_lines)
        for i in range(n_contour_lines):
            (
                levelset,
                pvalue,
            ) = self.distribution.computeMinimumVolumeLevelSetWithThreshold(
                self.contoursAlpha[i]
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

    def computeOutlierIndices(self, outlierFlag=True):
        """Get inlier or outlier indices.

        Outliers correspond to the :attr:`self.outlierAlpha` probability.

        :param bool outlierFlag: Whether to return outlier or inlier indices.
        :return: Outlier or inlier indices.
        :rtype: list(int)
        """
        flag = self.outlier_levelset.contains(self.sample)

        if outlierFlag:
            sample_idx = np.where(np.array(flag) == 0)[0]
        else:
            sample_idx = np.where(np.array(flag) != 0)[0]
        indices = [int(i) for i in sample_idx]

        return indices

    def setnumberOfPointsInXAxis(self, numberOfPointsInXAxis):
        self.numberOfPointsInXAxis = numberOfPointsInXAxis

    def getnumberOfPointsInXAxis(self):
        return self.numberOfPointsInXAxis

    def setnumberOfPointsInYAxis(self, numberOfPointsInYAxis):
        self.numberOfPointsInYAxis = numberOfPointsInYAxis

    def getnumberOfPointsInYAxis(self):
        return self.numberOfPointsInYAxis

    def setContoursAlpha(self, contoursAlpha):
        self.contoursAlpha = contoursAlpha

    def getContoursAlpha(self):
        return self.contoursAlpha

    def setOutlierAlpha(self, outlierAlpha):
        self.outlierAlpha = outlierAlpha

    def getOutlierAlpha(self):
        return self.outlierAlpha

    def _inliers_outliers(self, sample, inliers=True):
        """Inliers or outliers cloud drawing.

        :param sample: Sample of size (n_samples, n_dims).
        :type sample: :class:`openturns.Sample`
        :param bool inliers: Whether to draw inliers or outliers.
        :return: OpenTURNS Cloud or Pair object if :attr:`dim` > 2.
        :rtype: :class:`openturns.Cloud` or :class:`openturns.Pairs`
        """
        # Perform selection
        if inliers:
            idx = self.computeOutlierIndices(False)
            legend = "Inliers at alpha=%.4f" % (self.outlierAlpha)
            marker_color = self.inlier_color
        else:
            idx = self.computeOutlierIndices()
            legend = "Outliers at alpha=%.4f" % (self.outlierAlpha)
            marker_color = self.outlier_color

        sample_selection = sample[idx, :]

        if sample_selection.getSize() == 0:
            return

        cloud = ot.Cloud(sample_selection, marker_color, self.data_marker, legend)
        return cloud

    def _drawInliers(self, sample):
        """Draw inliers.

        :param sample: Sample of size (n_samples, n_dims).
        :type sample: :class:`openturns.Sample`
        :return: OpenTURNS Cloud or Pair object if :attr:`self.dim` > 2.
        :rtype: :class:`openturns.Cloud` or :class:`openturns.Pairs`
        """
        return self._inliers_outliers(sample, inliers=True)

    def _drawOutliers(self, sample):
        """Draw outliers.

        :param sample: Sample of size (n_samples, n_dims).
        :type sample: :class:`openturns.Sample`
        :return: OpenTURNS Cloud or Pair object if :attr:`self.dim` > 2.
        :rtype: :class:`openturns.Cloud` or :class:`openturns.Pairs`
        """
        return self._inliers_outliers(sample, inliers=False)

    def draw(self, drawInliers=False, drawOutliers=True):
        """Draw contour.

        If :attr:`drawData`, the whole sample is drawn. Otherwise, depending on
        :attr:`drawOutliers` it will either show the outliers or the inliers
        only.

        :param bool drawInliers: If True, plot inliers.
        :param bool drawOutliers: If True, plot outliers.
        :returns: figure, axes and OpenTURNS Graph object.
        :rtypes: Matplotlib figure instances, Matplotlib AxesSubplot instances,
          :class:`openturns.Graph`
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
                    pdf_graph = self.distribution.getMarginal(i).drawPDF()
                    graph.add(pdf_graph)

                elif i > j:  # lower corners
                    # Use a regular grid to compute probability response surface
                    X1min = self.sample[:, i].getMin()[0]
                    X1max = self.sample[:, i].getMax()[0]
                    X2min = self.sample[:, j].getMin()[0]
                    X2max = self.sample[:, j].getMax()[0]

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

                    data = self.distribution.getMarginal([i, j]).computePDF(xy)

                    # Label using percentage instead of probability
                    n_contours = len(self.contoursAlpha)
                    labels = [
                        "%.0f %%" % (self.contoursAlpha[i] * 100)
                        for i in range(n_contours)
                    ]

                    contour = ot.Contour(
                        xx, yy, data, self.pvalues, ot.Description(labels)
                    )
                    contour.setColor(self.contour_color)

                    graph.add(contour)

                    sample_ij = self.sample[:, [i, j]]

                    if drawInliers:
                        cloud = self._drawInliers(sample_ij)

                        if cloud is not None:
                            graph.add(cloud)

                    if drawOutliers:
                        cloud = self._drawOutliers(sample_ij)
                        if cloud is not None:
                            graph.add(cloud)

                if j == 0 and i > 0:
                    graph.setYTitle(plabels[j])
                if i == (self.dim - 1):
                    graph.setXTitle(plabels[i])

                if i >= j:  # lower triangle
                    graph.setLegends([""])
                    grid.setGraph(i, j, graph)

        return grid
