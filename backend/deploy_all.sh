#!/bin/bash
number=$1
./deploy.sh create_comment $1
./deploy.sh create_publication $1 
./deploy.sh get_comments $1
./deploy.sh get_publications $1 