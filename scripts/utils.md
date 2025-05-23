# Helpfull commands

Create VMs
```bash
uv run pxm-create -n 10 --config [path_to_config.json]
```

Start VMs
```bash
uv run pxm-start
```

Update package
```bash
bash scripts/run_commands.sh "source flexfl/venv/bin/activate && pip install --upgrade flexfl"
```

Check version
```bash
bash scripts/run_commands.sh -v "source flexfl/venv/bin/activate && pip freeze" | grep FlexFL
```

Clear results
```bash
bash scripts/run_commands.sh "rm -rf flexfl/results"
```

Send dataset
```bash
bash scripts/send_dataset.sh [dataset]
```

Gather results
```bash
bash scripts/gather_results.sh
```

Kill VMs processes
```bash
bash scripts/run_commands.sh "pkill -f flexfl"
```

Sync Workers clocks
```bash
bash scripts/run_commands.sh -w "sudo chronyc makestep"
```

Check Workers clocks
```bash
bash scripts/run_commands.sh -v -w "chronyc tracking"
```

Run FL in VMs
```bash
bash scripts/run_on_vms [interval] [change] [args]
```

With MPI
```bash
bash scripts/run_on_vms_mpi [args]
```

Containers
```bash
docker-compose -f requirements/kafka-compose.yml down --volumes --remove-orphans
docker-compose -f requirements/mqtt-compose.yml down --volumes --remove-orphans
source scripts/set_ip.sh 
docker-compose -f requirements/kafka-compose.yml up -d
docker-compose -f requirements/mqtt-compose.yml up -d
```

Remove .gitignore from results
```bash
find results -name ".gitignore" -type f -delete
```

Reset known_hosts
```bash
bash scripts/run_commands.sh -f scripts/known_hosts.sh
```