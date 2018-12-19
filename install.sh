#!/bin/bash
sudo apt-get install mysql-server build-essential python-dev php-mysql python-setuptools
#mysql -u root -h localhost -p
#CREATE USER pi@localhost IDENTIFIED BY pi;

###### HTML-Graph darstellung ######
 sudo apt-get install lighttpd php-cgi
 sudo lighttpd-enable-mod fastcgi fastcgi-php userdir      #   enable user dir ~/* to accept requests like 
 sudo service lighttpd force-reload                            #    http://xx.xx.xx.xx/~pi/*
####################################
#installiert python-libs und Adafruit DHT22 library

cd /home/pi/git-working-dir/
git clone https://github.com/getarun/shell-scripts
cd shell-scripts
chmod +x *.sh
./install-mysql-connector-python.sh                                #installiert myssql-connector for python
./install-adafruit-dht22.sh                                 #adafruit dht22 libraries

cd /home/pi/git-working-dir/RPi
# sudo cp data.php /var/www
# sudo cp create-graph.html /var/www
# sudo cp control.py /usr/bin                     #is in update-local-files.sh
# sudo cp phpinfo.php /var/www
# sudo chmod +x /usr/bin/control.py
# sudo chown www-data:www-data /var/www

sudo sh ./update-local-files.sh
