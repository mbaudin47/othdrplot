# coding: utf8
"""
Setup script for othdrplot
==========================

This script allows to install othdrplot within the python environment.

Usage
-----
::

    python setup.py install

"""
from setuptools import (setup, find_packages, Command)

setup_requires = ['pytest-runner']
tests_require = ['pytest', 'coverage']
install_requires = ['numpy>=1.13',
                    'matplotlib>=2.1',
                    'openturns']
extras_require = {'doc': ['sphinx>=1.4', 'nbsphinx', 'jupyter', 'jupyter_client']}

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='othdrplot',
    keywords=("surrogate model"),
    version='1',
    packages=find_packages(exclude=['doc']),
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    # Package requirements
    setup_requires=setup_requires,
    tests_require=tests_require,
    install_requires=install_requires,
    extras_require=extras_require,
    # metadata
    # maintainer="...",
    # maintainer_email="...",
    description="othdrplot: HDR plot",
    long_description=long_description,
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'License :: OSI Approved',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'Natural Language :: English',
                 'Operating System :: Unix',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Topic :: Documentation :: Sphinx',
                 'Topic :: Software Development',
                 'Topic :: Scientific/Engineering',
                 ],
    include_package_data=True,
    zip_safe=False,
    license="LGPL",
    url="http://www.openturns.org",
)
