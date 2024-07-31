#!/bin/bash -l

# Echo to stdout:
echo "process_netcdf_info_sbatch_slurm.sh: $@"

# Submit batch script to Slurm
sbatch $@
