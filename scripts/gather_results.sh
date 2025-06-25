#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

VM_LIST="scripts/ips.txt" # needs to end in empty line
# VM_LIST="vms/ips.txt"
USERNAME=$VM_USERNAME
PASSWORD=$VM_PASSWORD
ARGS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -q"

if [ ! -f "$VM_LIST" ]; then
    echo "Error: VM list file '$VM_LIST' not found!"
    exit 1
fi

function copy_results {
    local IP=$1
    echo "Copying results from $IP..."
    sshpass -p "$PASSWORD" scp $ARGS -r "$USERNAME@$IP:~/flexfl/results" "."
    if [ $? -eq 0 ]; then
        echo "Results copied from $IP successfully!"
    else
        echo "Failed to copy results from $IP!"
    fi
}

while read -r IP; do
    if [[ -z "$IP" || "$IP" =~ ^# ]]; then
        continue
    fi
    copy_results "$IP" &
done < "$VM_LIST"
wait
echo "Results copying completed!"

# echo "Cleaning remote files..."
# bash scripts/run_commands.sh "rm -rf flexfl/results" > /dev/null 2>&1
