#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

VM_LIST="scripts/ips.txt" # needs to end in empty line
# VM_LIST="vms/ips.txt"
USERNAME=$VM_USERNAME
PASSWORD=$VM_PASSWORD
ARGS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -q"
DATASET=$1

if [ -z "$DATASET" ]; then
    echo "Usage: $0 <dataset>"
    exit 1
fi

if [ ! -d "data/$DATASET" ]; then
    echo "Error: Dataset folder 'data/$DATASET' not found!"
    exit 1
fi

if [ ! -f "$VM_LIST" ]; then
    echo "Error: VM list file '$VM_LIST' not found!"
    exit 1
fi

function send_dataset {
    local IP=$1
    local NODE_ID=$2

    echo "Sending dataset $DATASET/node_$NODE_ID to $IP..."
    sshpass -p "$PASSWORD" ssh -n $ARGS "$USERNAME@$IP" "mkdir -p ~/flexfl/data/$DATASET" > /dev/null 2>&1 &&
    sshpass -p "$PASSWORD" scp $ARGS -r "data/$DATASET/node_$NODE_ID" "$USERNAME@$IP:~/flexfl/data/$DATASET" > /dev/null 2>&1 &&
    sshpass -p "$PASSWORD" ssh -n $ARGS "$USERNAME@$IP" "mv ~/flexfl/data/$DATASET/node_$NODE_ID ~/flexfl/data/$DATASET/my_data" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Dataset sent to $IP successfully!"
    else
        echo "Failed to send dataset to $IP!"
    fi
}

NODE_ID=0
while read -r IP; do
    if [[ -z "$IP" || "$IP" =~ ^# ]]; then
        continue
    fi
    send_dataset "$IP" "$NODE_ID" &
    NODE_ID=$((NODE_ID + 1))
done < "$VM_LIST"
wait
echo "Dataset setup completed!"

