#!/bin/bash

WORKERS=$1
INTERVAL=$2
CHANCE=$3
shift 3
RUN_ARGS=$@

if ! [[ "$INTERVAL" =~ ^[0-9]+(\.[0-9]+)?$ && "$CHANCE" =~ ^[0-9]+(\.[0-9]+)?$ && "$WORKERS" =~ ^[0-9]+$ ]]; then
    echo "Error: Workers, interval and chance must be numbers."
    exit 1
fi

echo "Killing all screen sessions..."
pkill screen > /dev/null 2>&1

echo "Running master..."
COMMAND="uv run flexfl --is_anchor --no-save_model $RUN_ARGS"
screen -dmS fl-master bash -c "$COMMAND"

echo "Waiting..."
sleep 10

function run_command {
    local WORKER_ID=$1
    echo "Running worker $WORKER_ID..."
    COMMAND="uv run flexfl-res -s $WORKER_ID -i $INTERVAL -c $CHANCE -w 3 uv run flexfl --results_folder worker_$WORKER_ID --data_folder node_$WORKER_ID $RUN_ARGS"
    screen -dmS fl-worker-$WORKER_ID bash -c "$COMMAND"
}

for (( WORKER_ID=1; WORKER_ID<=$WORKERS; WORKER_ID++ )); do
    sleep 1
    run_command "$WORKER_ID" 
done
wait
echo "Command execution completed!"
