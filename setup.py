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

install_requires = ['numpy>=1.13',
                    'matplotlib>=2.1',
                    'openturns>=1.14'
                    ]
extras_require = {'doc': ['sphinx>=1.4', 'nbsphinx', 'jupyter', 'jupyter_client']}

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='othdrplot',
    keywords=("graphics"),
    version='0.2.3',
    packages=find_packages(exclude=['doc']),
    install_requires=install_requires,
    extras_require=extras_require,
    description="othdrplot: HDR plot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'License :: OSI Approved',
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
    zip_safe=False,
    license="LGPL",
    url="https://github.com/mbaudin47/othdrplot",
)
