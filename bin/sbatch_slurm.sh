#!/bin/bash -l

# Echo to stdout:
echo "sbatch_slurm.sh: $@"

# Submit batch script to Slurm
sbatch $@
