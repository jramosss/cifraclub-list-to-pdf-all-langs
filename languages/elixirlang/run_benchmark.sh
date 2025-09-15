#!/bin/bash

# Not working yet, can't make chromium work
exit 0

IMAGE_NAME="elixir_benchmark"
CONTAINER_NAME="elixir_benchmark_runner"
OUTPUT_FILE="benchmarks.json"
WORKDIR="/app"

docker build --platform=linux/arm64 -t $IMAGE_NAME .

docker run --name $CONTAINER_NAME $IMAGE_NAME

docker cp $CONTAINER_NAME:$WORKDIR/$OUTPUT_FILE .

docker rm $CONTAINER_NAME