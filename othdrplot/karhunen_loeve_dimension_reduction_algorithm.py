# -*- coding: utf-8 -*-
# Copyright 2018 - 2021 EDF.
"""
Reduces the dimensionnality of a process sample with K-L decomposition.
"""
import openturns as ot


class KarhunenLoeveDimensionReductionAlgorithm:
    """KarhunenLoeveDimensionReductionAlgorithm."""

    def __init__(self, processSample, numberOfComponents):
        """
        Reduces the dimension of a process sample from KL.

        Parameters
        ----------
        processSample : ot.ProcessSample
            The collection of processes.
        """
        self.processSample = processSample
        self.numberOfComponents = numberOfComponents

    def run(self):
        """
        Run high density region algorithm.
        """
        # KL decomposition
        threshold = 0.0
        algo = ot.KarhunenLoeveSVDAlgorithm(self.processSample, threshold)
        algo.setNbModes(self.numberOfComponents)
        algo.run()
        karhunenLoeveResult = algo.getResult()
        self.reducedComponents = karhunenLoeveResult.project(self.processSample)
        numberOfComponents = self.reducedComponents.getDimension()
        labels = ["C" + str(i) for i in range(numberOfComponents)]
        self.reducedComponents.setDescription(labels)

    def getReducedComponents(self):
        """
        Returns the reduced components.

        Returns
        -------
        reducedComponents : ot.Sample(n, d)
            The n points in the d-dimensional reduced space.
        """
        return self.reducedComponents
