#!/bin/bash

# make sure we source the 
source home/michael/eups/desdm_eups_setup.sh 

setup desdmdashboard trunk+0

python $1
