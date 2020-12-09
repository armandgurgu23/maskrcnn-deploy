#!/bin/bash

docker run -e SERVER_MODE=$1 --attach $2 --publish 8000:6969 $3:$4 --restart $5