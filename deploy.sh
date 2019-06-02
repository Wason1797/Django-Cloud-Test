#!/bin/bash

# necesary variables to know where to locate the files
echo Enter the container folder name
read main_folder
echo Enter the git url to clone
read repo_url
echo Enter the project folder
read project_folder 
echo Enter the project name
read project_name 


working_path="/home/ubuntu/$main_folder"


mkdir $main_folder

# clone the git repo with the project
cd $main_folder
git clone $repo_url

cd ..
chmod -R 777 $main_folder/
cd $main_folder

echo Copy secrets.json to the project folder
read line

# install necesary packages

sudo apt-get install python3-pip supervisor python-virtualenv
sudo apt-get install nginx libpq-dev python3-dev

virtualenv venv --python=python3

source "./venv/bin/activate"

# install requirements and gunicorn
cd $project_folder

pip3 install -r requirements.txt
pip3 install gunicorn


# configuring supervisor

cd /etc/supervisor/conf.d/

sudo rm gunicorn.conf
sudo touch gunicorn.conf

sudo cat << EOF > gunicorn.conf
[program:gunicorn]
directory=${working_path}/${project_folder}/${project_name}
command=${working_path}/venv/bin/gunicorn --workers 3 --bind unix:${working_path}/${project_folder}/${project_name}/app.sock ${project_name}.wsgi:application
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn/gunicorn.err.log
stdout=logfile=/var/log/gunicorn/gunicorn.out.log

[group:guni]
programs:gunicorn
EOF

sudo mkdir /var/log/gunicorn
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all
sudo supervisorctl status

# configuring nginx, server name needs change
cd /etc/nginx/sites-available/
sudo rm django.conf
sudo touch django.conf

sudo cat << EOF > django.conf
server {
        listen 80 ;
        server_name ; 

        location / {
            include proxy_params;
            proxy_pass http://unix:${working_path}/${project_folder}/${project_name}/app.sock;
        }

        
}
EOF

sudo rm /etc/nginx/sites-enabled/django.conf
sudo ln django.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo service nginx restart


