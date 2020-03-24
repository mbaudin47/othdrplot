#!/bin/bash

set -xe
export PYTHONPATH="$PWD:$PYTHONPATH"
cd tests && bash run-all.sh && cd -

