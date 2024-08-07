#!/bin/bash -l

echo "CCR_module_test.sh: $@"

# For module testing on CCR.
# Note: this module test assumes that you have cloned the https://github.com/GhubGateway/CCR_Ghub_Demo Github repository.

# Usage:
# Login to CCR OnDemand.
# Launch a Quick Launch General-Compute Desktop Interactive App.
# Open a terminal window (Click the >_ button).
# In the terminal window, change directory (cd) to the CCR_Ghub_Demo/module_tests directory.
# Enter: source CCR_module_test.sh

start=$(date +%s)

modeling_group_path='/projects/grid/ghub/ISMIP6/Projections/Reprocessed/CMIP6_Archive_Final/AIS/AWI'

source ../bin/pythonLaunch.sh ../bin/get_netcdf_info.py $modeling_group_path

# See the CCR_Ghub_Demo/module_tests directory for output files:
# AIS_AWI_netcdf_info.json and AIS_AWI_netcdf_info.txt

end=$(date +%s)
elapsed_time_sec=$((end-start))
secs_to_mins=0.0166667
echo "$elapsed_time_sec $secs_to_mins" | awk '{printf "elasped time: %.2f [min]\n", $1*$2}'
