#!/bin/bash

# We require the -it flag to run a reactJS app as described here
# https://github.com/facebook/create-react-app/issues/8688
docker run --env-file ./container.env -it --detach --publish $1:3000 $2:$3 --restart $4