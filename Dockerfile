# Setting up the entire Health Activity Monitoring Application in one container for simplicity.
#
# VERSION           0.1

FROM ubuntu:latest
MAINTAINER  Manuel Maldonado <mo.maldonado@gmail.com>

# Intall apache2
RUN sudo apt-get -y install apache2

# Install Mongo
RUN sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen ' | sudo tee /etc/apt/sources.list.d/mongodb.list
RUN sudo apt-get update
RUN sudo apt-get -y install mongodb-org mongodb-org-server
RUN mkdir /data
RUN mkdir /data/db

# Install PHP
RUN sudo apt-get -y install php5 php5-dev libapache2-mod-php5 apache2-threaded-dev php-pear php5-mongo

# Install MongoDB PHP Module
RUN sudo pecl install mongo
RUN sudo echo "extension=mongo.so" >> /etc/php5/apache2/php.ini
RUN sudo service apache2 restart

# Add needed information for testing
RUN sudo echo "<?php phpinfo(); ?>" > /var/www/html/phpinfo.php

# Install Redis Server
RUN sudo apt-get -y install redis-server

# Install Python
RUN sudo apt-get -y install wget build-essential checkinstall
RUN sudo apt-get -y install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
RUN sudo mkdir /Downloads
WORKDIR /Downloads/
RUN wget http://python.org/ftp/python/2.7.10/Python-2.7.10.tgz
RUN tar -xvf Python-2.7.10.tgz
WORKDIR ./Python-2.7.10/
RUN ls -ltrh
RUN ./configure
RUN make
RUN sudo checkinstall -y
WORKDIR /Downloads/
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

# Configure Python
RUN pip install twitter 
RUN pip install prettytable 
RUN pip install tweepy 
RUN pip install flask 
RUN pip install redis 
RUN pip install pymongo==2.7.2
# json Counters

# Add application files
ADD www/ /var/www/html

# Add application files
RUN mkdir /home/python
ADD CalorieMeter/ /home/python
ADD data_filtering/ /home/python
ADD interactive_map/Demo2/ /home/python

# Add the command to run
ADD start.sh /home/python/
RUN chmod 777 /home/python/start.sh

# Docker-specific properties
EXPOSE 80
EXPOSE 5000
WORKDIR /home/python
ENTRYPOINT ["sh", "-c", "/home/python/start.sh"]