#!/bin/bash

if [ -z ${IMAGE_TAG} ]
then
  read -p "Enter Image Tag: " IMAGE_TAG
fi

sudo docker build -f ./dockerfiles/th3-server/Dockerfile . -t docker.io/tlee75/th3-server:${IMAGE_TAG}
