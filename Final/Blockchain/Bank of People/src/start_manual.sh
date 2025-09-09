#!/bin/bash

cd ./images
./build.sh

cd ../challenge-eth
sudo docker pull docker.io/dimasmaualana/eth:latest
sudo docker compose up --build