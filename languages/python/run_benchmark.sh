#!/bin/bash

# Check if --local flag is provided
if [[ "$1" == "--local" ]]; then
    echo "Running Python benchmark locally..."
    pip install -r requirements.txt
    python benchmark.py
else
    IMAGE_NAME="python_benchmark"
    CONTAINER_NAME="python_benchmark_runner"
    OUTPUT_FILE="benchmarks.json"
    WORKDIR="/app"

    docker build --platform=linux/arm64 -t $IMAGE_NAME .

    docker run --name $CONTAINER_NAME $IMAGE_NAME

    docker cp $CONTAINER_NAME:$WORKDIR/$OUTPUT_FILE .

    docker rm $CONTAINER_NAME
fi