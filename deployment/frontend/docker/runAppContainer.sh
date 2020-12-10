#!/bin/bash

docker run --env-file ./container.env --detach --publish $1:3000 $2:$3 --restart $4