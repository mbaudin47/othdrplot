# -*- coding: utf-8 -*-
"""
Generate a 2D sample made of a mixture of two bivariate gaussian variables. 
"""
import openturns as ot
from openturns import Graph, Cloud
from openturns.viewer import View

# Create a Funky distribution
corr = ot.CorrelationMatrix(2)
corr[0, 1] = 0.2
copula = ot.NormalCopula(corr)
x1 = ot.Normal(-1.0, 1)
x2 = ot.Normal(2, 1)
x_funk = ot.ComposedDistribution([x1, x2], copula)

# Create a Punk distribution
x1 = ot.Normal(1.0, 1)
x2 = ot.Normal(-2, 1)
x_punk = ot.ComposedDistribution([x1, x2], copula)

# Merge the distributions
mixture = ot.Mixture([x_funk, x_punk], [0.5, 1.0])

# Sample from the mixture
ns = 1000
sample = mixture.getSample(ns)

# Draw a scatter plot
graph = Graph("Data", "X1", "X2", True, "")
cloud = Cloud(sample, "blue", "fsquare", "My Cloud")
graph.add(cloud)
View(graph).show()

sample.exportToCSVFile("gauss-mixture-2D.csv")
