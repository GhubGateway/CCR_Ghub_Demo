#!/bin/bash -l

# For interim testing on CCR.

# Created the python environment cccghubdemo to install packages required but not in python/3.9.6.

tool_alias_name=ccrghubdemo
build_version=v1

#Ghub:
#Pegasus workflow in progress...
#/projects/grid/ghub/ISMIP6/Projections/Reprocessed/CMIP6_Archive_Final/AIS
#Antarctica
#AWI,ILTS_PIK

start=$(date +%s)

# Activate the venv
module load ccrsoft/2023.01
module load gcc/11.2.0
module load python/3.9.6
source /projects/grid/ghub/Tools/${tool_alias_name}/${build_version}/software/2023.01/python/venv/bin/activate
which python

#python ./get_netcdf_info.py '/projects/grid/ghub/ISMIP6/Projections/Reprocessed/CMIP6_Archive_Final/AIS/AWI'
python ./get_netcdf_info.py '/projects/grid/ghub/ISMIP6/Projections/Reprocessed/CMIP6_Archive_Final/AIS/ILTS_PIK'

end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"

deactivate
