#!/bin/bash

# we need to source the eups setup script first
source /eeups/eups/desdm_eups_setup.sh

setup desdmdashboard trunk+0

python $1
