#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 [-v] [-w] [-f] <command>"
    echo "  -v: verbose mode"
    echo "  -w: run command only on workers (skip first line of ips.txt)"
    echo "  -f: run a script file on the VMs"
    echo "  use options by order: -v -w -f"
    exit 1
fi

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

VM_LIST="scripts/ips.txt" # needs to end in empty line
# VM_LIST="vms/ips.txt"
USERNAME=$VM_USERNAME
PASSWORD=$VM_PASSWORD
ARGS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -q"
VERBOSE=0
ONLY_WORKERS=0

if [ "$1" == "-v" ]; then
    VERBOSE=1
    shift
fi
if [ "$1" == "-w" ]; then
    ONLY_WORKERS=1
    shift
fi
COMMAND=$@

RUN_FILE=0
if [ "$1" == "-f" ]; then
    FILE=$2
    RUN_FILE=1
    shift 2
    COMMAND="sudo bash /tmp/$FILE $@"
    if [ ! -f "$FILE" ]; then
        echo "Error: File $FILE not found."
        exit 1
    fi
fi

echo "Command to execute: $COMMAND"

function run_command {
    local IP=$1
    if [ $RUN_FILE -eq 1 ]; then
        sshpass -p "$PASSWORD" scp $ARGS "$VM_LIST" "$USERNAME@$IP:~/$VM_LIST"
        sshpass -p "$PASSWORD" ssh $ARGS "$USERNAME@$IP" "mkdir -p /tmp/scripts"
        sshpass -p "$PASSWORD" scp $ARGS "$FILE" "$USERNAME@$IP:/tmp/$FILE"
    fi
    if [ $VERBOSE -eq 0 ]; then
        sshpass -p "$PASSWORD" ssh -tt $ARGS "$USERNAME@$IP" "bash -i -c '$COMMAND'" > /dev/null 2>&1
    else
        sshpass -p "$PASSWORD" ssh -tt $ARGS "$USERNAME@$IP" "bash -i -c '$COMMAND'"
    fi
    if [ $? -eq 0 ]; then
        echo "Command executed successfully on $IP."
    else
        echo "Error: Command failed on $IP."
    fi
}

read -r MASTER_IP < "$VM_LIST"

while read -r IP; do
    if [ $ONLY_WORKERS -eq 1 ] && [ "$IP" == "$MASTER_IP" ]; then
        continue
    fi
    if [[ -z "$IP" || "$IP" =~ ^# ]]; then
        continue
    fi
    run_command "$IP" &
done < "$VM_LIST"
wait
echo "Command execution completed!"