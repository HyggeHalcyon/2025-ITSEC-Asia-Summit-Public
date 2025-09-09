#!/bin/bash

cd ./images
./build.sh

cd ../challenge-eth
sudo docker compose up --build