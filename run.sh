# Decentralized Synchronous
bash scripts/run_on_vms_mpi.sh --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds --base_dir mpi_ds_1
bash scripts/run_on_vms_mpi.sh --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds --base_dir mpi_ds_2
bash scripts/run_on_vms_mpi.sh --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds --base_dir mpi_ds_3
bash scripts/run_on_vms_mpi.sh --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds --base_dir mpi_ds_4

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c zenoh --base_dir zenoh_ds_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c zenoh --base_dir zenoh_ds_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c zenoh --base_dir zenoh_ds_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c zenoh --base_dir zenoh_ds_4

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c mqtt --base_dir mqtt_ds_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c mqtt --base_dir mqtt_ds_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c mqtt --base_dir mqtt_ds_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c mqtt --base_dir mqtt_ds_4

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c kafka --base_dir kafka_ds_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c kafka --base_dir kafka_ds_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c kafka --base_dir kafka_ds_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c kafka --base_dir kafka_ds_4

# Decentralized Asynchronous
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_da_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_da_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_da_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_da_4

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_da_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_da_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_da_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_da_4

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_da_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_da_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_da_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_da_4

# Centralized Synchronous
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c zenoh --base_dir zenoh_cs_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c zenoh --base_dir zenoh_cs_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c zenoh --base_dir zenoh_cs_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c zenoh --base_dir zenoh_cs_4

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c mqtt --base_dir mqtt_cs_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c mqtt --base_dir mqtt_cs_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c mqtt --base_dir mqtt_cs_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c mqtt --base_dir mqtt_cs_4

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c kafka --base_dir kafka_cs_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c kafka --base_dir kafka_cs_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c kafka --base_dir kafka_cs_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c kafka --base_dir kafka_cs_4

# Centralized Asynchronous
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c zenoh --base_dir zenoh_ca_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c zenoh --base_dir zenoh_ca_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c zenoh --base_dir zenoh_ca_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c zenoh --base_dir zenoh_ca_4

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c mqtt --base_dir mqtt_ca_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c mqtt --base_dir mqtt_ca_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c mqtt --base_dir mqtt_ca_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c mqtt --base_dir mqtt_ca_4

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c kafka --base_dir kafka_ca_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c kafka --base_dir kafka_ca_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c kafka --base_dir kafka_ca_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c kafka --base_dir kafka_ca_4

# With failures
# Zenoh
bash scripts/run_on_vms.sh 1 0.005 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_f05
bash scripts/run_on_vms.sh 1 0.01 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_f1
bash scripts/run_on_vms.sh 1 0.03 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_f3

# MQTT
bash scripts/run_on_vms.sh 1 0.005 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_f05
bash scripts/run_on_vms.sh 1 0.01 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_f1
bash scripts/run_on_vms.sh 1 0.03 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_f3

# Kafka
bash scripts/run_on_vms.sh 1 0.005 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_f05
bash scripts/run_on_vms.sh 1 0.01 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_f1
bash scripts/run_on_vms.sh 1 0.03 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_f3

# With 40 workers
bash scripts/run_on_vms.sh 1 0.01 --min_workers 28 --learning_rate 0.0001 --epochs 20 --patience 20 --fl da -c zenoh -d unsw --base_dir zenoh_unsw_40
bash scripts/run_on_vms.sh 1 0.01 --min_workers 28 --learning_rate 0.0001 --epochs 20 --patience 20 --fl da -c zenoh -d ton_iot --base_dir zenoh_ton_iot_40