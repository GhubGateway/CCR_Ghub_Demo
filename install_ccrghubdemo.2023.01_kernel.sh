#!/bin/bash -l

# Usage:
# source install_ccrghubdemo.2023.01_kernel.sh

# Create the Python environment

tool_alias_name=ccrghubdemo
build_version=v1

SOFTWARE_PATH=/projects/grid/ghub/Tools/${tool_alias_name}/${build_version}/software
echo 'SOFTWARE_PATH: '${SOFTWARE_PATH}

module load ccrsoft/2023.01
module load gcccore/11.2.0
module load python/3.9.6
module load ipython/7.26.0

source ${SOFTWARE_PATH}/2023.01/python/venv/bin/activate

echo "which python3: "$(which python3)
echo "which jupyter: "$(which jupyter)

python3 -m ipykernel install --user --name ccrghubdemo_kernel

# Note: to uninstall the kernel
#jupyter kernelspec uninstall ccrghubdemo_kernel

jupyter kernelspec list

deactivate
