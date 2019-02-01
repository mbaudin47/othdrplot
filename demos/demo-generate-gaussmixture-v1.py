#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2018 EDF.
"""
Demonstration de Kernel Smoothing 2D avec OpenTURNS.
Etant donné α dans (0,1), on recherche p dans (0,1) tel que 

P(X dans A(p)) = α 

où 

A(p)={X dans Rn tel que f(x) > p}.

Etant donné α, on cherche le seuil p tel que 
la probabilité d'avoir une densité de points 
supérieure à p est égal à α.


Pour OpenTURNS v1.8
Michael Baudin, 2017
"""

import openturns as ot
from openturns import (Graph, Cloud)
# Pour afficher les graphes
from openturns.viewer import View

# 1.1 Create a Funky distribution
R = ot.CorrelationMatrix(2)
R[0, 1] = 0.2
copula = ot.NormalCopula(R)
X1=ot.Normal(-1.,1)
X2=ot.Normal(2,1)
XFunk = ot.ComposedDistribution([X1, X2], copula)

# 1.2 Create a Punk distribution
X1=ot.Normal(1.,1)
X2=ot.Normal(-2,1)
XPunk = ot.ComposedDistribution([X1, X2], copula)

# 1.3 Merge the distributions
X = ot.Mixture([XFunk,XPunk], [0.5,1.])

# 2. Draw a scatter plot
N=1000 # Number of points in the sample
data = X.getSample(N)

# 3. Draw a scatter plot
myGraph = Graph("Data", "X1", "X2", True, '')
myCloud = Cloud(data, 'blue', 'fsquare', 'My Cloud')
myGraph.add(myCloud)
View(myGraph).show()

data.exportToCSVFile("gauss-mixture.csv")
