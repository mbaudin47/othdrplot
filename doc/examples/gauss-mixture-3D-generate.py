# -*- coding: utf-8 -*-
"""
Generate a 3D sample made of a mixture of two gaussian variables. 
"""

import openturns as ot
from openturns.viewer import View

# Create a Funky distribution
corr = ot.CorrelationMatrix(3)
corr[0, 1] = 0.2
corr[1, 2] = -0.3
copula = ot.NormalCopula(corr)
x1 = ot.Normal(-1.0, 1)
x2 = ot.Normal(2, 1)
x3 = ot.Normal(-2, 1)
x_funk = ot.ComposedDistribution([x1, x2, x3], copula)

# Create a Punk distribution
x1 = ot.Normal(1.0, 1)
x2 = ot.Normal(-2, 1)
x3 = ot.Normal(3, 1)
x_punk = ot.ComposedDistribution([x1, x2, x3], copula)

# Merge the distributions
distribution = ot.Mixture([x_funk, x_punk], [0.5, 1.0])

# Sample from the mixture
n = 500
sample = distribution.getSample(n)

myGraph = ot.Graph("Sample n=%d" % (n), " ", " ", True, "")
myPairs = ot.Pairs(sample, "Pairs", sample.getDescription(), "blue", "bullet")
myGraph.add(myPairs)
View(myGraph)

sample.exportToCSVFile("gauss-mixture-3D.csv")
