#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

VM_LIST="scripts/ips.txt" # needs to end in empty line
VM_LIST="vms/ips.txt"
USERNAME=$VM_USERNAME
PASSWORD=$VM_PASSWORD
ARGS="-n -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -q"
INTERVAL=$1
CHANCE=$2
shift 2
RUN_ARGS=$@

if ! [[ "$INTERVAL" =~ ^[0-9]+(\.[0-9]+)?$ && "$CHANCE" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    echo "Error: Interval and chance must be float numbers."
    exit 1
fi

if [ ! -f "$VM_LIST" ]; then
    echo "Error: VM list file '$VM_LIST' not found!"
    exit 1
fi

echo "Killing all sessions..."
bash scripts/run_commands.sh "pkill -f flexfl" > /dev/null 2>&1

read -r MASTER_IP < "$VM_LIST"

function run_command {
    local IP=$1
    local WORKER_ID=$2
    echo "Running command on $IP..."
    COMMAND="cd flexfl && source venv/bin/activate && flexfl-res -s $WORKER_ID -i $INTERVAL -c $CHANCE -w 10 flexfl --results_folder worker_$WORKER_ID --ip \"$MASTER_IP\" --data_folder my_data $RUN_ARGS"
    sshpass -p "$PASSWORD" ssh $ARGS "$USERNAME@$IP" "screen -dmS fl-worker-$WORKER_ID bash -c \"$COMMAND\""
}

echo "Running command on master..."
INFO="interval_{$INTERVAL}_chance_{$CHANCE}"
# --no-save_model
COMMAND="cd flexfl && source venv/bin/activate && flexfl --is_anchor --data_folder my_data --info $INFO $RUN_ARGS"
sshpass -p "$PASSWORD" ssh $ARGS "$USERNAME@$MASTER_IP" "screen -dmS fl-master bash -c \"$COMMAND\""

echo "Waiting..."
sleep 5

WORKER_ID=1
while read -r IP_; do
    if [[ -z "$IP_" || "$IP_" =~ ^# ]]; then
        continue
    fi
    run_command "$IP_" "$WORKER_ID" &
    WORKER_ID=$((WORKER_ID + 1))
done < <(tail -n +2 "$VM_LIST")
wait
echo "Command execution completed!"

sshpass -p "$PASSWORD" ssh -tt $ARGS "$USERNAME@$MASTER_IP" "screen -r fl-master"

echo "Done!"
