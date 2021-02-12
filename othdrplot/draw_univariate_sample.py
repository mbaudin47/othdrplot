#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 23:30:42 2021

@author: devel
"""
import openturns as ot


def DrawUnivariateSampleDistribution(sample, distribution):
    """
    Draw a unidimensional sample and its distribution.
    
    Parameters
    ----------
    sample : ot.Sample
        A dimension 1 sample.
    distribution : ot.Distribution
        A dimension 1 distribution.

    Returns
    -------
    graph : ot.Graph
        The PDF plot and the sample on the X axis.
    """
    if sample.getDimension()!=1:
        raise ValueError("Expect a 1 dimension sample, but dimension is %d" % (sample.getDimension()))
    if distribution.getDimension()!=1:
        raise ValueError("Expect a 1 dimension distribution, but dimension is %d" % (distribution.getDimension()))
    graph = distribution.drawPDF()
    # Add points on X axis
    sample_size = sample.getSize()
    data = ot.Sample(sample_size, 2)
    data[:, 0] = sample
    cloud = ot.Cloud(data)
    graph.add(cloud)
    return graph
