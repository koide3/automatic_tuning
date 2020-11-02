#!/bin/bash
docker run -it --rm \
           -v $(realpath ..):/automatic_tuning \
           -v ~/datasets:/datasets \
           -v $(realpath ../docker/LeGO-LOAM-BOR):/root/catkin_ws/src/LeGO-LOAM-BOR \
           -w /automatic_tuning/scripts \
           automatic_tuning \
           $@
