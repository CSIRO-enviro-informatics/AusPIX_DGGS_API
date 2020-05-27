#!/bin/bash
yum update -y
amazon-linux-extras install docker 
yum -y install git
curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
chmod +x /usr/bin/docker-compose
systemctl enable docker
systemctl start docker && sleep 5
echo "vm.max_map_count=262144" >> /etc/sysctl.d/98-sysctl.conf
usermod -a -G docker ec2-user
git clone --single-branch --branch prod https://github.com/CSIRO-enviro-informatics/AusPIX_DGGS_API.git
mv /tmp/instance.sh  /var/lib/cloud/scripts/per-instance/instance.sh
mv /tmp/wildcard-loci-cat.bundle.pem /home/ec2-user/AusPIX_DGGS_API/certs/
mv /tmp/wildcard-loci-cat.pem /home/ec2-user/AusPIX_DGGS_API/certs/
ls -la /home/ec2-user/AusPIX_DGGS_API/certs/
chmod +x /var/lib/cloud/scripts/per-instance/instance.sh
