#!/bin/bash
cd /home/pi/git-working-dir/RPi

sudo cp data.php /var/www
sudo cp create-graph.html /var/www
sudo cp control.py /usr/bin
sudo cp about.php /var/www

sudo chmod +x /usr/bin/control.py

sudo chown www-data:www-data /var/www

sudo cp manpage.man /usr/share/man/control.1
