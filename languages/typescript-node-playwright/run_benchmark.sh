#!/bin/bash

IMAGE_NAME="typescript_node_benchmark"
CONTAINER_NAME="typescript_node_benchmark_runner"
OUTPUT_FILE="benchmarks.json"
WORKDIR="/app"

docker build --platform=linux/arm64 -t $IMAGE_NAME .

docker run --name $CONTAINER_NAME $IMAGE_NAME

docker cp $CONTAINER_NAME:$WORKDIR/$OUTPUT_FILE .

docker rm $CONTAINER_NAME