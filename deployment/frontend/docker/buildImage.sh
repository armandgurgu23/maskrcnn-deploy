#!/bin/bash

docker build -f ./Dockerfile -t $1:$2 ../../../ && docker images

