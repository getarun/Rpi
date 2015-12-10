#!/bin/bash
##################
#echo "Use this to Copy Lokal Git Repo in RPi to SD"
#echo "Only use with working versions annotated with tags >= v1.0"
##################

cd /home/pi/git-working-dir/RPi
echo "update-local-files: source: /home/pi/git-working-dir/RPi"
echo "Copying data.php, create-graph.html, about.php to webserver (/var/www)"
sudo cp data.php /var/www
sudo cp create-graph.html /var/www
sudo cp about.php /var/www
sudo chown www-data:www-data /var/www

#echo("Copying control.py to local bin-tree (/usr/bin)")
sudo cp control.py /usr/bin
sudo chmod +x /usr/bin/control.py
