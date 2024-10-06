#!/bin/bash
number=$1
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $1.dkr.ecr.us-east-1.amazonaws.com
./deploy.sh create_comment $1
sleep 10
./deploy.sh create_publication $1 
sleep 10
./deploy.sh get_comments $1
sleep 10
./deploy.sh get_publications $1 
sleep 10