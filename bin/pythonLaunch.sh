#!/bin/bash -l

echo "pythonLaunch.sh: $@"

tool_alias_name=ccrghubdemo
build_version=v1

# Activate the Python environment

module load ccrsoft/2023.01
module load gcccore/11.2.0
module load python/3.9.6
source /projects/grid/ghub/Tools/${tool_alias_name}/${build_version}/software/2023.01/python/venv/bin/activate
which python

# Wait for job to finish
python "$@"

deactivate

exit 0
