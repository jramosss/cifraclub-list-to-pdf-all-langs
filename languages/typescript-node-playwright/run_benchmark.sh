#!/bin/bash

# Check if --local flag is provided
if [[ "$1" == "--local" ]]; then
    echo "Running TypeScript Node benchmark locally..."
    npm install
    npm run build-and-run
else
    IMAGE_NAME="typescript_node_benchmark"
    CONTAINER_NAME="typescript_node_benchmark_runner"
    OUTPUT_FILE="benchmarks.json"
    WORKDIR="/app"

    docker build --platform=linux/arm64 -t $IMAGE_NAME .

    docker run --name $CONTAINER_NAME $IMAGE_NAME

    docker cp $CONTAINER_NAME:$WORKDIR/$OUTPUT_FILE .

    docker rm $CONTAINER_NAME
fi