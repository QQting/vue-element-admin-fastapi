#!/bin/bash

WORK_DIR=$PWD
export LD_LIBRARY_PATH=$WORK_DIR/app/app/api/api_v1/robots/RMT_core/
python $WORK_DIR/app/app/main.py
