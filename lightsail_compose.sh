#!/bin/bash

# install latest version of docker the lazy way
curl -sSL https://get.docker.com | sh

# make it so you don't need to sudo to run docker commands
usermod -aG docker ubuntu

# install docker-compose
curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# copy the dockerfile into /srv/docker 
# if you change this, change the systemd service file to match
WorkingDirectory=/var/city_climate
# curl -o /var/docker/compose.yaml.yml https://github.com/guszejnovdavid/City_Climate_WebApp/raw/main/compose.yaml
cd var
git clone http://github.com/guszejnovdavid/City_Climate_WebApp.git $WorkingDirectory

# copy in systemd unit file and register it so our compose file runs 
# on system restart
curl -o /etc/systemd/system/docker-compose-app.service https://github.com/guszejnovdavid/City_Climate_WebApp/raw/main/docker-compose-app.service
systemctl enable docker-compose-app

# start up the application via docker-compose
docker-compose -f $WorkingDirectory/compose.yaml up -d