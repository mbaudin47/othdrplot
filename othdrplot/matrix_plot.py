# -*- coding: utf-8 -*-
# Copyright 2019 EDF-CERFACS.
"""
Component to create MatrixPlot.
"""
import openturns as ot
import matplotlib.pyplot as plt
import openturns.viewer as otv

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

    def draw(self, figsize = (10, 10)):
        """

        :returns: figure, axes and OpenTURNS Graph object.
        :rtypes: Matplotlib figure instances, Matplotlib AxesSubplot instances,
          :class:`openturns.Graph`
        """
        fig = plt.figure(figsize = figsize)
        # Axis are created and stored top to bottom, left to right
        for i in range(self.dim):
            for j in range(self.dim):
                k = i + j * self.dim + 1

                if i <= j:  # lower triangle
                    ax = fig.add_subplot(self.dim, self.dim, k)
                    graph = ot.Graph('', '', '', True, 'topright')

                if i == j:  # diag
                    if (self.distribution is None):
                        factory = ot.KernelSmoothing()
                        distribution = factory.build(self.sample[:, i])
                        estimatedDistribution_graph = distribution.drawPDF()
                        estimatedDistribution_graph.setLegends([''])
                        graph.add(estimatedDistribution_graph)
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
                _ = otv.View(graph, figure=fig, axes=[ax])

        return fig    
