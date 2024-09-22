#!/bin/bash
name=$1
number=$2
docker build -t $name . --build-arg LAMBDA_FILE=$name.py
docker tag $name:latest $number.dkr.ecr.us-east-1.amazonaws.com/$name:latest
docker push $number.dkr.ecr.us-east-1.amazonaws.com/$name:latest