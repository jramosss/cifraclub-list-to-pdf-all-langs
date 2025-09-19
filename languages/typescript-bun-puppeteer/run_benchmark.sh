#!/bin/bash

# Check if --local flag is provided
if [[ "$1" == "--local" ]]; then
    echo "Running TypeScript Bun benchmark locally..."
    bun install
    bun start
else
    IMAGE_NAME="typescript_bun_benchmark"
    CONTAINER_NAME="typescript_bun_benchmark_runner"
    OUTPUT_FILE="benchmarks.json"
    WORKDIR="/app"

    docker build --platform=linux/arm64 -t $IMAGE_NAME .

    docker run --name $CONTAINER_NAME $IMAGE_NAME

    docker cp $CONTAINER_NAME:$WORKDIR/$OUTPUT_FILE .

    docker rm $CONTAINER_NAME
fi