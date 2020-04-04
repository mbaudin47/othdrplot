#!/bin/sh

set -xe

echo "Python interpreter"
echo `which python`
echo "Jupyter"
echo `which jupyter`
echo "OpenTURNS version"
python -c "import openturns; print(openturns.__version__); exit()"

# Run tests
cd ..

python doc/examples/demo-matrixplot.py

# Unit tests
cd tests
python -m unittest discover .
cd ..

# Notebooks in all subdirectories
python tests/find-ipynb-files.py
