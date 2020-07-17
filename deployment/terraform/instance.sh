#!/bin/bash
# On first instance creation this script will execute to execute the docker-compose command that bootstraps / first executes the application on instance creation
# subsequent execution after a reboot should happen via container restart policies 
cd /home/ec2-user/AusPIX_DGGS_API/ && docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d 
