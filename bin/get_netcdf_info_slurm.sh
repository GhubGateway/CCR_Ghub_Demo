#!/bin/bash -l

#SBATCH --time=00:30:00
#SBATCH --nodes=1-1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name="ccrghubdemo"
#SBATCH --output="ccrghubdemo-%j_out.txt"
#SBATCH --mail-user=renettej@buffalo.edu
#SBATCH --mail-type=fail
#SBATCH --cluster=ub-hpc
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute

echo "get_netcdf_info_slurm.sh: $@"

launch_script=$1
echo "launch_script: "$launch_script
job_script=$2
echo "job_script: "$job_script
modeling_group_path=$3
echo "modeling_group_path: "$modeling_group_path

# See: https://docs.hpc.shef.ac.uk/en/latest/referenceinfo/scheduler/SLURM/SLURM-environment-variables.html#gsc.tab=0
#echo "SLURM_JOBID="$SLURM_JOBID
#echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST
#echo "SLURM_NNODES"=$SLURM_NNODES
#echo "SLURM_NTASKS"=$SLURM_NTASKS
#echo "SLURMTMPDIR="$SLURMTMPDIR

$launch_script $job_script $modeling_group_path
