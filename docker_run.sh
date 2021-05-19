#!/bin/bash
docker_name="prisoners_dilemma_tournament"

docker build -t "$docker_name" .
docker run -v "$PWD":/opt -it "$docker_name"
