#!/bin/bash 

INSTANCE_URL=ubuntu@ec2-52-37-61-214.us-west-2.compute.amazonaws.com
PEM_NAME="aws-ec2-gat1.pem"

echo "SETTING UP"

SCRIPT='
sudo apt-get update;
sudo apt-get upgrade;
sudo apt-get install nginx;
sudo apt-get install postgresql postgresql-contrib
sudo passwd postgres
#enter sudo password
#unix password- postgres
#unix password - postgres
su - postgres
#password is postgres

sudo -u postgres createdb lucas

sudo -u postgres psql -U postgres -d lucas -f "/home/ubuntu/Projects/GAT/sql/create_t_account.sql"
sudo -u postgres psql -U postgres -d lucas -f "/home/ubuntu/Projects/GAT/sql/create_t_session.sql"

sudo sed -i "1s/.*/user ubuntu;/" /etc/nginx/nginx.conf;
sudo sed -i "/# server_names_hash_bucket_size 64;/a server_names_hash_bucket_size 128;" /etc/nginx/nginx/conf;

cd;
mkdir Projects;
cd Projects;
mkdir GAT;
sudo ln -sT ~/Projects/GAT /var/www/html/GAT;
'

ssh -i "${PEM_NAME}" "${INSTANCE_URL}" "${SCRIPT}"

echo "COPYING NGINX FILES"

scp -i "${PEM_NAME}" virtual.conf "${INSTANCE_URL}":~

COPY_SCRIPT="
sudo mv ~/virtual.conf /etc/nginx/conf.d/ 
"

ssh -i "${PEM_NAME}" "${INSTANCE_URL}" "${COPY_SCRIPT}"

echo "FINISHED SETUP"
