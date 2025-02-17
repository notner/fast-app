#!/bin/bash

cd ../
python -m build
docker build -t 'myapp-0.0.1' .
echo 'run with docker run myapp-0.0.1'
