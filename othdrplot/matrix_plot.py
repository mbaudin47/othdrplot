# -*- coding: utf-8 -*-
# Copyright 2019 EDF-CERFACS.
"""
Component to create MatrixPlot.
"""
import openturns as ot
import matplotlib.pyplot as plt
from openturns.viewer import View


class MatrixPlot:
    """MatrixPlot."""

    def __init__(self, sample, distribution=None):
        """Matrix plot with density on the diagonal.

        :param sample: Sample of size (n_samples, n_dims).
        :param distribution: Probability Density Function of the sample.
        :type sample: :class:`openturns.Sample`
        :type distribution: :class:`openturns.Distribution`
        """
        self.sample = sample
        self.distribution = distribution
        self.dim = sample.getDimension()
        self.size = sample.getSize()
        self.labels = sample.getDescription()

    def draw(self):
        """

        :returns: figure, axes and OpenTURNS Graph object.
        :rtypes: Matplotlib figure instances, Matplotlib AxesSubplot instances,
          :class:`openturns.Graph`
        """
        fig = plt.figure(figsize=(10, 10))
        sub_ax = []  # Axis stored as a list
        sub_graph = []
        # Axis are created and stored top to bottom, left to right
        for i in range(self.dim):
            for j in range(self.dim):
                k = i + j * self.dim + 1

                if i <= j:  # lower triangle
                    ax = fig.add_subplot(self.dim, self.dim, k)
                    graph = ot.Graph('', '', '', True, 'topright')

                if i == j:  # diag
                    if (self.distribution is None):
                        histo_graph = ot.HistogramFactory().build(self.sample[:, i]).drawPDF()
                        histo_graph.setLegends([''])
                        graph.add(histo_graph)
                    else:
                        pdf_graph = self.distribution.getMarginal(i).drawPDF()
                        pdf_graph.setLegends([''])
                        graph.add(pdf_graph)

                elif i < j:  # lower corners
                    cloud = ot.Cloud(self.sample[:, i], self.sample[:, j])
                    graph.add(cloud)

                if i == 0:
                    graph.setYTitle(self.labels[j])
                if j == (self.dim - 1):
                    graph.setXTitle(self.labels[i])

                graph.setLegends([''])
                sub_graph.append(ot.viewer.View(graph, figure=fig, axes=[ax]))
                sub_ax.append(ax)

        return fig, sub_ax, sub_graph
