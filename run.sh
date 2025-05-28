# Decentralized Synchronous
bash scripts/run_on_vms_mpi.sh --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds --base_dir mpi_ds_1
bash scripts/run_on_vms_mpi.sh --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds --base_dir mpi_ds_2
bash scripts/run_on_vms_mpi.sh --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds --base_dir mpi_ds_3
bash scripts/run_on_vms_mpi.sh --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds --base_dir mpi_ds_4
bash scripts/run_on_vms_mpi.sh --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds --base_dir mpi_ds_5

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c zenoh --base_dir zenoh_ds_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c zenoh --base_dir zenoh_ds_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c zenoh --base_dir zenoh_ds_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c zenoh --base_dir zenoh_ds_4
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c zenoh --base_dir zenoh_ds_5

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c mqtt --base_dir mqtt_ds_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c mqtt --base_dir mqtt_ds_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c mqtt --base_dir mqtt_ds_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c mqtt --base_dir mqtt_ds_4
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c mqtt --base_dir mqtt_ds_5

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c kafka --base_dir kafka_ds_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c kafka --base_dir kafka_ds_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c kafka --base_dir kafka_ds_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c kafka --base_dir kafka_ds_4
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ds -c kafka --base_dir kafka_ds_5

# Decentralized Asynchronous
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_da_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_da_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_da_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_da_4
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_da_5

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_da_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_da_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_da_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_da_4
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_da_5

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_da_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_da_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_da_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_da_4
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_da_5

# Centralized Synchronous
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c zenoh --base_dir zenoh_cs_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c zenoh --base_dir zenoh_cs_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c zenoh --base_dir zenoh_cs_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c zenoh --base_dir zenoh_cs_4
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c zenoh --base_dir zenoh_cs_5

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c mqtt --base_dir mqtt_cs_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c mqtt --base_dir mqtt_cs_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c mqtt --base_dir mqtt_cs_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c mqtt --base_dir mqtt_cs_4
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c mqtt --base_dir mqtt_cs_5

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c kafka --base_dir kafka_cs_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c kafka --base_dir kafka_cs_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c kafka --base_dir kafka_cs_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c kafka --base_dir kafka_cs_4
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl cs -c kafka --base_dir kafka_cs_5

# Centralized Asynchronous
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c zenoh --base_dir zenoh_ca_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c zenoh --base_dir zenoh_ca_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c zenoh --base_dir zenoh_ca_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c zenoh --base_dir zenoh_ca_4
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c zenoh --base_dir zenoh_ca_5

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c mqtt --base_dir mqtt_ca_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c mqtt --base_dir mqtt_ca_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c mqtt --base_dir mqtt_ca_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c mqtt --base_dir mqtt_ca_4
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c mqtt --base_dir mqtt_ca_5

bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c kafka --base_dir kafka_ca_1
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c kafka --base_dir kafka_ca_2
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c kafka --base_dir kafka_ca_3
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c kafka --base_dir kafka_ca_4
bash scripts/run_on_vms.sh 0 0 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl ca -c kafka --base_dir kafka_ca_5

# With failures
# Zenoh
bash scripts/run_on_vms.sh 1 0.005 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_f05_1
bash scripts/run_on_vms.sh 1 0.005 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_f05_2
bash scripts/run_on_vms.sh 1 0.005 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_f05_3

bash scripts/run_on_vms.sh 1 0.01 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_f1_1
bash scripts/run_on_vms.sh 1 0.01 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_f1_2
bash scripts/run_on_vms.sh 1 0.01 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_f1_3

bash scripts/run_on_vms.sh 1 0.02 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_f2_1
bash scripts/run_on_vms.sh 1 0.02 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_f2_2
bash scripts/run_on_vms.sh 1 0.02 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c zenoh --base_dir zenoh_f2_3

# MQTT
bash scripts/run_on_vms.sh 1 0.005 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_f05_1
bash scripts/run_on_vms.sh 1 0.005 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_f05_2
bash scripts/run_on_vms.sh 1 0.005 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_f05_3

bash scripts/run_on_vms.sh 1 0.01 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_f1_1
bash scripts/run_on_vms.sh 1 0.01 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_f1_2
bash scripts/run_on_vms.sh 1 0.01 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_f1_3

bash scripts/run_on_vms.sh 1 0.02 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_f2_1
bash scripts/run_on_vms.sh 1 0.02 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_f2_2
bash scripts/run_on_vms.sh 1 0.02 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c mqtt --base_dir mqtt_f2_3

# Kafka
bash scripts/run_on_vms.sh 1 0.005 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_f05_1
bash scripts/run_on_vms.sh 1 0.005 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_f05_2
bash scripts/run_on_vms.sh 1 0.005 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_f05_3

bash scripts/run_on_vms.sh 1 0.01 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_f1_1
bash scripts/run_on_vms.sh 1 0.01 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_f1_2
bash scripts/run_on_vms.sh 1 0.01 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_f1_3

bash scripts/run_on_vms.sh 1 0.02 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_f2_1
bash scripts/run_on_vms.sh 1 0.02 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_f2_2
bash scripts/run_on_vms.sh 1 0.02 --min_workers 7 --learning_rate 0.0001 --patience 10 --fl da -c kafka --base_dir kafka_f2_3

