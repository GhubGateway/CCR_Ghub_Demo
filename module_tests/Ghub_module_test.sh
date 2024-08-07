#!/bin/bash

echo "Ghub_module_test.sh: $@"

# For module testing on Ghub.
# Note: this module test assumes that you have cloned the https://github.com/GhubGateway/CCR_Ghub_Demo Github repository.
# Note: you must be a member of the Ghub submit group to run this script.

# Usage:
# Login to Ghub.
# Launch the Workspace 10 Tool.
# In the terminal window, change directory (cd) to the CCR_Ghub_Demo/module_tests directory.
# Enter: source Ghub_module_test.sh

start=$(date +%s)

modeling_group_path='/projects/grid/ghub/ISMIP6/Projections/Reprocessed/CMIP6_Archive_Final/AIS/AWI'

# The submit command below, takes the ../remotebin/pythonLaunch.sh bash script and executes it remotely on CCR, and,
# blocks until ../remotebin/pythonLaunch.sh completes execution.
# See https://help.hubzero.org/documentation/22/tooldevs/grid/submitcmd for more information.

# Options:
# -v, --venue: Remote job destination
# -w, --wallTime: Estimated walltime hh:mm:ss or minutes
# -i, --inputfile: Input File

submit -v ccr-vortex-ghub -w 10 -i ../bin/get_netcdf_info.py ../remotebin/pythonLaunch.sh get_netcdf_info.py $modeling_group_path

# See the CCR_Ghub_Demo/module_tests directory for output files:
# AIS_AWI_netcdf_info.json and AIS_AWI_netcdf_info.txt

end=$(date +%s)
elapsed_time_sec=$((end-start))
secs_to_mins=0.0166667
echo "$elapsed_time_sec $secs_to_mins" | awk '{printf "elasped time: %.2f [min]\n", $1*$2}'
