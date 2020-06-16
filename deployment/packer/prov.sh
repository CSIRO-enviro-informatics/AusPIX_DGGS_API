#!/bin/bash
# configure the aws machine ready to start the DGGS API via instance.sh
# note instance.sh will only run once at instance creation time to bootstrap initial container creation 
# subsequent manual reboots should leverage docker restart policies to recreate containers

#install and configure docker and docker compose to run on startup  
yum update -y
amazon-linux-extras install docker 
yum -y install git
curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
chmod +x /usr/bin/docker-compose
systemctl enable docker
systemctl start docker && sleep 5
usermod -a -G docker ec2-user

# clone the master branch of the AusPIX_DGGS_API from github locally, this effects "installation" of the AusPIX_DGGS_API on the ec2 machine ready to run
git clone --single-branch --branch master https://github.com/CSIRO-enviro-informatics/AusPIX_DGGS_API.git
# move ssh certs to the directory expected by AusPIX_DIGGS_API docker compose  
mkdir /home/ec2-user/AusPIX_DGGS_API/certs/
mv /tmp/wildcard-loci-cat.bundle.pem /home/ec2-user/AusPIX_DGGS_API/certs/
mv /tmp/wildcard-loci-cat.pem /home/ec2-user/AusPIX_DGGS_API/certs/