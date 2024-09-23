#!/bin/bash
# mv .env .env.dev
# cp .env.prod .env
# npm run build

# number=$1
# docker build -t frontend . 
# docker tag frontend:latest $number.dkr.ecr.us-east-1.amazonaws.com/frontend:latest
# docker push $number.dkr.ecr.us-east-1.amazonaws.com/frontend:latest

# mv .env.dev .env

bucket_name=$1
npm run build
aws s3 cp build s3://$1 --recursive