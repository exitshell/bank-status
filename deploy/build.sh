#!/usr/bin/env bash

echo -e "-- Building application containers --\n"

# Stop docker containers.
docker-compose stop -t 1

# Build docker images from source code.
docker-compose build

# Push docker images to dockerhub registry.
docker-compose push

echo -e "\n-- Application containers have been built and pushed --"
