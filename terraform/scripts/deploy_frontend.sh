#!/bin/bash
bucket_name=$1
backend_url=$2
cd ./../frontend
echo PUBLIC_BASE_PATH=$backend_url > .env
npm install
npm run build
aws s3 cp build s3://$1 --recursive