#!/bin/bash -l

# Echo to stdout:
echo "get_netcdf_info_sbatch_slurm.sh: $@"

# Submit batch script to Slurm
sbatch $@
