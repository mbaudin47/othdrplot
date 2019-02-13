|CI|_ |Python|_ |License|_

.. |CI| image:: https://circleci.com/gh/tupui/othdrplot.svg?style=svg
.. _CI: https://circleci.com/gh/tupui/othdrplot

.. |Python| image:: https://img.shields.io/badge/python-2.7,_3.7-blue.svg
.. _Python: https://python.org

.. |License| image:: https://img.shields.io/badge/license-LGPL-blue.svg
.. _License: https://opensource.org/licenses/LGPL

otHDRPlot
=========

What is it?
-----------

This project implements the Functional highest density region boxplot technique [Hyndman2009]_.
It is based on `OpenTURNS <http://www.openturns.org>`_.

When you have functional data, which is to say: a curve, you will want to answer
some questions such as:

* What is the median curve?
* Can I draw a confidence interval?
* Or, is there any outliers?

This module allows you to do exactly this: 

.. code-block:: python

    hdr = ProcessHighDensityRegionAlgorithm(sample)
    hdr.setOutlierAlpha(0.8)
    hdr.run()
    hdr.plotOutlierTrajectories()

The output is the following figure: 

.. image::  doc/images/npfda-elnino-OutlierTrajectoryPlot.png

Requirements
------------

The dependencies are: 

- Python >= 2.7 or >= 3.3
- `numpy <http://www.numpy.org>`_ >= 0.10
- `OpenTURNS <http://www.openturns.org>`_ >= 1.12
- `matplotlib <https://matplotlib.org>`_ >= 1.5.3

References
----------

.. [Hyndman2009] Rob J Hyndman and Han Lin Shang. Rainb ow plots , bagplots and b oxplots for functional data. Journal of Computational and Graphical Statistics, 19:29-45, 2009
