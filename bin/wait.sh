#!/bin/bash -l

# Echo to stdout:
#echo "wait.sh: $@"

username=$1
#echo "usersname: "$username
wait_min=$2
#echo "waiting: "$wait_min" [m]"
# wait in 15 second intervals
wait_intervals=$(( wait_min * 4 ))
#echo "waiting up to: "$wait_intervals", 15 second intervals"
# Wait for batch jobs to complete
exitCode=1
for (( i = 0; i < $wait_intervals; i++ ))
do
    check=$(squeue --user=$username)
    #echo $check
    if [[ $check == *"ccrghub"* ]]; then
        echo "Waiting for batch job(s) to complete..."
        sleep 15 # seconds
    else
        echo "Done!"
        exitCode=0
        break
    fi
done

exit $exitCode
