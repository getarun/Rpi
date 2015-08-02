#!/bin/bash
# do once
# git clone git://github.de/getarun/RPi
cd RPi
sudo cp data.php /var/www
sudo cp create-graph.html /var/www
sudo cp control.py /usr/bin
git pull
