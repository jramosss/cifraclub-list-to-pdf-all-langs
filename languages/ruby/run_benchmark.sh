#!/bin/bash

# Check if --local flag is provided
if [[ "$1" == "--local" ]]; then
    echo "Running Ruby benchmark locally..."
    bundle install
    ruby benchmark.rb
else
    IMAGE_NAME="ruby_benchmark"
    CONTAINER_NAME="ruby_benchmark_runner"
    OUTPUT_FILE="benchmarks.json"
    WORKDIR="/app"

    docker build --platform=linux/arm64 -t $IMAGE_NAME .

    docker run --name $CONTAINER_NAME $IMAGE_NAME

    docker cp $CONTAINER_NAME:$WORKDIR/$OUTPUT_FILE $OUTPUT_FILE

    docker rm $CONTAINER_NAME
fi