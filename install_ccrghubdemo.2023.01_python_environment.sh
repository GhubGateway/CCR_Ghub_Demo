#!/bin/bash -l

# Usage:
# source install_ccrghubdemo.2023.01_python_environment.sh

# Create the Python environment

tool_alias_name=ccrghubdemo
build_version=v1

SOFTWARE_PATH=/projects/grid/ghub/Tools/${tool_alias_name}/${build_version}/software
echo 'SOFTWARE_PATH: '${SOFTWARE_PATH}

module load ccrsoft/2023.01
module load gcccore/11.2.0
module load python/3.9.6

rm -rf ${SOFTWARE_PATH}/2023.01/python/venv
python -m venv ${SOFTWARE_PATH}/2023.01/python/venv
source ${SOFTWARE_PATH}/2023.01/python/venv/bin/activate
pip install --upgrade pip
pip install hublib
pip install netcdf4
pip install xarray
pip install tabulate
pip install openpyxl

deactivate
