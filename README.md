# FL_Benchmark
This repository is a code basis to create and compare different FL approaches.

## Installation
If you are on Windows, you can use the WSL to run the code. To install the WSL, you can use the following commands:
```bash
wsl --install
```

### Docker
To install docker, you can use the following commands:
```bash
# install docker
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# post installation
sudo groupadd docker
sudo usermod -aG docker $USER
```

To run the code in a docker container, you can use the following commands:
```bash
# create the docker image (it may take a while)
docker build -t fl_benchmark .
# create the docker container
docker run -d --name fl_benchmark fl_benchmark
# start the container if it is not running
docker start fl_benchmark
# go to the container
docker exec -it fl_benchmark bash
```

### Local
To run the code locally, you can use the following commands:
```bash
# install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y libopenmpi-dev python3 python3-pip
# create a virtual environment
python3 -m venv venv
# activate the virtual environment
source venv/bin/activate
# install the requirements (it may take a while)
pip install -r requirements.txt
```

## Post Installation
Some datasets are downloaded from kaggle, so you need to create a kaggle account and key. After that create a file named `.env` in the root directory with the following content:
```bash
KAGGLE_USERNAME="<username>"
KAGGLE_KEY="<key>"
```

## Usage
To run the code, you can use the following commands:
```bash
# download the datasets
python3 Programs/preprocess.py -d all
# divide the datasets
python3 Programs/division.py -d all -n 0
# run the federated learning
mpirun -n 5 python3 Programs/fl.py --dataset IOT_DNL
# or from a file
mpirun -n 5 python3 Programs/fl.py --file example.json
# arguments can be overwritten example:
mpirun -n 5 python3 Programs/fl.py --file example.json --dataset IOT_DNL
# to see the help
python3 Programs/fl.py -h
```
