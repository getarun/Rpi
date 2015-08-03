#!/bin/bash



cd /home/pi/RPi
sudo cp data.php /var/www
sudo cp create-graph.html /var/www
sudo cp control.py /usr/bin
sudo chown www-data:www-da /var/www
