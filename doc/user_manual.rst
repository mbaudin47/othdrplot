========================
Documentation of the API
========================

This is the user manual for the Python bindings to the othdrplot library.

How does it work?
-----------------

Behind the scene, the dataset is represented as a matrix. Each line corresponding
to a 1D curve. This matrix is then decomposed using Principal Components Analysis (PCA).
This allows to represent the data using a finit number of modes, or components.
This compression process allows to turn the functional representation into a
scalar representation of the matrix. In other words, you can visualize each curve
from its components. This is called a bivariate plot.

.. image::  images/npfda-elnino-DensityPlot.png

This visualization exhibit a cluster of points. It indicate that a lot of
curve lead to a common components. The center of the cluster is the mediane curve.
An the more you get away from the cluster, the more the curve is unlikely to be
similar to the other curves.

Using a kernel smoothing technique, the probability density function (PDF) of
the 2D space can be recover. From this PDF, it is possible to compute the density
probability linked to the cluster and plot its contours.

Finally, using these contours, the different quantiles are extracted allong with
the mediane curve and the outliers.

.. image::  images/npfda-elnino-OutlierTrajectoryPlot.png


.. currentmodule:: othdrplot

otHDRPlot
=========

.. autosummary::
    :toctree: _generated/
    :template: class.rst_t
    :nosignatures:

    HighDensityRegionAlgorithm
    ProcessHighDensityRegionAlgorithm
