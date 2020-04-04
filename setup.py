# coding: utf-8
"""
Setup script for othdrplot
==========================

This script allows to install othdrplot within the python environment.

Usage
-----
::

    python setup.py install

"""
from setuptools import (setup, find_packages)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='othdrplot',
    keywords=("graphics"),
    version='1.0.1',
    packages=find_packages(),
    install_requires=['numpy',
                      'matplotlib',
                      'openturns'
                      ],
    description="High Density Region plot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'Natural Language :: English',
                 'Operating System :: Unix',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3',
                 'Topic :: Documentation :: Sphinx',
                 'Topic :: Software Development',
                 'Topic :: Scientific/Engineering',
                 ],
    include_package_data=True,
    package_data={'othdrplot': ['othdrplot/data/*.csv']},
    license="LGPL",
    url="https://github.com/mbaudin47/othdrplot",
    author="Michaël Baudin and Pamphile Roy",
    author_email="michael.baudin@gmail.com", 
)
