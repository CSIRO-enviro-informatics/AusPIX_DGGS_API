#!/bin/bash
cd /home/ec2-user/AusPIX_DGGS_API/ && pwd && ls && while [ ! -d "./certs" ];  do sleep 2; done; docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d 
