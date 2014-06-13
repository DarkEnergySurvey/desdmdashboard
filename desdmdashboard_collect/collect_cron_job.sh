#!/bin/bash

# we need to source the eups setup script first
source /eeups/eups/desdm_eups_setup.sh
# add the path of this script to the pythonpath
MY_PATH="`dirname \"$0\"`"
MY_PATH="`( cd \"$MY_PATH\" && pwd )`"
export PYTHONPATH=$PYTHONPATH:$MY_PATH

setup desdmdashboard trunk+0

python $1
