#!/bin/bash -l

# Echo to stdout:
echo "sbatch_slurm.sh: $@"

# Submit batch script to Slumr
sbatch $@

# Wait for batch job to complete
for k in {1..12};
do
    check=$(squeue --user=renettej)
    #echo $check
    if [[ $check == *"ccrghub"* ]]; then
        echo "Waiting for batch job to complete..."
        sleep 10
    else
        echo "Done!"
        break
    fi
done
