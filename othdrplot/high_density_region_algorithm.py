# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Component to create HighDensityRegionAlgorithm.
"""
import numpy as np
import openturns as ot


class HighDensityRegionAlgorithm:
    """Compute the Highest Density Region."""

    def __init__(self, sample, distribution):
        """Compute a High Density Region.

        :param sample: Sample of size (n_samples, n_dims).
        :param distribution: Probability Density Function of the sample.
        :type sample: :class:`openturns.Sample`
        :type distribution: :class:`openturns.Distribution`
        """
        # Number of points per dim to plot the contour
        self.numberOfPointsInXAxis = 30
        self.numberOfPointsInYAxis = 30

        # The list of probabilities to create the contour
        self.contoursAlpha = [0.9, 0.5, 0.1]
        self.outlierAlpha = 0.9  # The probability for outlier detection

        self.data_marker = "fsquare"  # The marker for data

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
            levelset, pvalue = self.distribution.computeMinimumVolumeLevelSetWithThreshold(
                self.contoursAlpha[i])
            self.pvalues[i] = pvalue
            self.levelsets.append(levelset)

        # Compute the outlier level set
        levelset, pvalue = self.distribution.computeMinimumVolumeLevelSetWithThreshold(
            self.outlierAlpha)

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

        return sample_idx

    def setnumberOfPointsInXAxis(self, numberOfPointsInXAxis):
        self.numberOfPointsInXAxis = numberOfPointsInXAxis

    def setnumberOfPointsInYAxis(self, numberOfPointsInYAxis):
        self.numberOfPointsInYAxis = numberOfPointsInYAxis

    def setContoursAlpha(self, contoursAlpha):
        self.contoursAlpha = contoursAlpha

    def setOutlierAlpha(self, outlierAlpha):
        self.outlierAlpha = outlierAlpha

    def _inliers_outliers(self, inliers=True):
        """Inliers or outliers cloud ploting.

        :param bool inliers: Whether to plot inliers or outliers.
        :return: OpenTURNS Cloud or Pair object if :attr:`self.dim` > 2.
        :rtype: :class:`openturns.Graph` or :class:`openturns.Pairs`
        """
        if inliers:
            idx = self.computeOutlierIndices(False)
            legend = "Inliers at alpha=%.4f" % (self.outlierAlpha)
            marker_color = 'blue'
        else:
            idx = self.computeOutlierIndices()
            legend = "Outliers at alpha=%.4f" % (self.outlierAlpha)
            marker_color = 'red'

        sample = np.array(self.sample)
        sample = sample[idx, :]

        if sample.size == 0:
            return

        if self.dim == 2:
            cloud = ot.Cloud(sample, marker_color, self.data_marker, legend)
        else:
            cloud = ot.Pairs(sample, '', self.sample.getDescription(),
                             marker_color, self.data_marker)

        return cloud

    def plotContour(self, plotData=False, plotOutliers=True):
        """Plot High Density Region.

        If :attr:`plotData`, the whole sample is drawn. Otherwise, depending on
        :attr:`plotOutliers` it will either show the outliers or the inliers
        only.

        :param bool plotData: Plot inliers and outliers.
        :param bool plotOutliers: Whether to plot inliers or outliers.
        :return: OpenTURNS Graph object.
        :rtype: :class:`openturns.Graph`
        """
        graph = ot.Graph('High Density Region plot', '', '', True, 'topright')

        if self.dim == 2:
            # Use a regular grid to compute probability response surface
            X1min = self.sample[:, 0].getMin()[0]
            X1max = self.sample[:, 0].getMax()[0]
            X2min = self.sample[:, 1].getMin()[0]
            X2max = self.sample[:, 1].getMax()[0]

            xx = ot.Box([self.numberOfPointsInXAxis],
                        ot.Interval([X1min], [X1max])).generate()

            yy = ot.Box([self.numberOfPointsInXAxis],
                        ot.Interval([X2min], [X2max])).generate()

            xy = ot.Box([self.numberOfPointsInXAxis, self.numberOfPointsInXAxis],
                        ot.Interval([X1min, X2min], [X1max, X2max])).generate()

            data = self.distribution.computePDF(xy)

            # Label using percentage instead of probability
            n_contours = len(self.contoursAlpha)
            labels = ["%.0f %%" % (self.contoursAlpha[i] * 100)
                      for i in range(n_contours)]

            contour = ot.Contour(xx, yy, data, self.pvalues,
                                 ot.Description(labels))
            contour.setColor('black')

            xlabel, ylabel = self.sample.getDescription()
            graph.setXTitle(xlabel)
            graph.setYTitle(ylabel)
            graph.add(contour)

        if plotData:
            graph.add(self._inliers_outliers(inliers=True))

            outliers = self._inliers_outliers(inliers=False)
            if outliers is not None:
                graph.add(outliers)
        elif plotOutliers:
            graph.add(self._inliers_outliers(inliers=True))
        else:
            outliers = self._inliers_outliers(inliers=False)
            if outliers is not None:
                graph.add(outliers)

        return graph
