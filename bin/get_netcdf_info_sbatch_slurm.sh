#!/bin/bash -l

# Echo to stdout:
echo "sbatch_slurm.sh: $@"

slurm_script=$1
#echo "slurm_script: "$slurm_script
launch_script=$2
#echo "launch_script: "$launch_script
job_script=$3
#echo "job_script: "$job_script
ice_sheet_folder=$4
#echo "ice_sheet_folder: "$ice_sheet_folder
modeling_groups=$5
#echo "modeling_groups: "$modeling_groups

IFS=',' read -ra array <<< $modeling_groups
#echo "${array[*]}"

# Submit batch scripts to Slurm
for modeling_group in "${array[@]}"
do
    #echo "modeling_group: "$modeling_group
    sbatch $slurm_script $launch_script $job_script $ice_sheet_folder$modeling_group
done

# Wait for batch jobs to complete
for k in {1..12};
do
    check=$(squeue --user=renettej)
    #echo $check
    if [[ $check == *"ccrghub"* ]]; then
        echo "Waiting for batch jobs to complete..."
        sleep 10
    else
        echo "Done!"
        break
    fi
done
