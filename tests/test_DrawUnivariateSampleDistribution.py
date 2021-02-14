# -*- coding: utf-8 -*-
# Copyright 2018 - 2021 EDF - CERFACS.
"""
Test for DrawUnivariateSampleDistribution class.
"""
import unittest
import openturns as ot
import othdrplot as othdr
import openturns.viewer as otv


class CheckDrawUnivariateSampleDistribution(unittest.TestCase):
    def test_DrawUnivariateSampleDistribution(self):
        sample = ot.Normal().getSample(500)

        # Distribution fit in reduced space
        ks = ot.KernelSmoothing()
        distribution = ks.build(sample)

        graph = othdr.DrawUnivariateSampleDistribution(sample, distribution)
        otv.View(graph)
        return


if __name__ == "__main__":
    unittest.main()
