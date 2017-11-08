#!/bin/bash

cd $(dirname $0)
python3 -m unittest discover -v "$(dirname $0)"/test
