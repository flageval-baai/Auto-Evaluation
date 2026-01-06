#!/bin/bash
current_file="$0"
current_dir="$(dirname "$current_file")"
SERVER_IP=$1
SERVER_PORT=$2
PYTHONPATH=$current_dir:$PYTHONPATH  accelerate launch $current_dir/model_adapter.py  --server_ip $SERVER_IP --server_port $SERVER_PORT "${@:3}" --cfg $current_dir/meta.json --no-local-mode
