#!/bin/bash

docker run --env-file ./container.env --detach --publish $1:6969 $2:$3 --restart $4