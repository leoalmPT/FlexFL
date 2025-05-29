#!/bin/bash

VM_LIST="scripts/ips.txt"

sudo apt update -y &&
sudo dpkg --configure -a &&
sudo apt upgrade -y &&

while read -r IP; do
    ssh-keyscan -H $IP >> ~/.ssh/known_hosts 2>/dev/null
done < "$VM_LIST" &&

sudo apt install -y python3.12-venv python3-dev libopenmpi-dev ntpsec &&
mkdir flexfl &&
cd flexfl &&
mkdir data &&
mkdir results &&
python3 -m venv venv &&
# echo "source $HOME/flexfl/venv/bin/activate" >> ~/.bashrc &&
source venv/bin/activate &&
pip install flexfl[all]

# check ntpsec
# ntpq -p

# sudo sysctl vm.swappiness=99