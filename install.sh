#!/bin/bash
sudo apt-get install mysql-server build-essential python-dev
#mysql -u root -h localhost -p
#CREATE USER pi@localhost IDENTIFIED BY pi;

###### HTML-Graph darstellung ######
 sudo apt-get install lighttpd php5-cgi
 sudo lighttpd-mod-enable fastcgi fastcgi-php #userdir      #   enable user dir ~/* to accept requests like 
 sudo service lighttpd force-reload                            #    http://xx.xx.xx.xx/~pi/*
####################################
#installiert python-libs und Adafruit DHT22 library
mkdir /home/pi/git-working-dir
cd /home/pi/git-working-dir
git clone https://github.com/getarun/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo pyhton setup.py install

cd /home/pi/git-working-dir
git clone https://github.com/getarun/shell-scripte
cd shell-scripte
./install-mysql-connector.sh

cd /home/pi/git-workings-dir/RPi
sudo cp data.php /var/www
sudo cp create-graph.html /var/www
sudo cp control.py /usr/bin
sudo chmod +x /usr/bin/control.py
sudo chown www-data:www-da /var/www
