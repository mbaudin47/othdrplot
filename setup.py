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
    version='1.0',
    packages=find_packages(exclude=['doc']),
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    # Package requirements
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
    url="https://github.com/mbaudin47/othdrplot",
)
