#!/bin/bash -l

#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name="ccrghubdemo"
#SBATCH --output="ccrghubdemo-%j_out.txt"
#SBATCH --cluster=ub-hpc
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute

echo "process_netcdf_info_slurm.sh: $@"

launch_script=$1
echo "launch_script: "$launch_script
job_script=$2
echo "job_script: "$job_script
ice_sheet_folder=$3
echo "ice_sheet_folder: "$jice_sheet_folder
ice_sheet_description=$4
echo "ice_sheet_description: "$ice_sheet_description
modeling_groups=$5
echo "modeling_groups: "$modeling_groups

# See: https://docs.hpc.shef.ac.uk/en/latest/referenceinfo/scheduler/SLURM/SLURM-environment-variables.html#gsc.tab=0
echo "SLURM_JOBID="$SLURM_JOBID

$launch_script $job_script $ice_sheet_folder $ice_sheet_description $modeling_groups
