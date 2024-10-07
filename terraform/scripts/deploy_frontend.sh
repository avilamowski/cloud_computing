#!/bin/bash
bucket_name=$1
cd ./../frontend
npm install
npm run build
aws s3 cp build s3://$1 --recursive