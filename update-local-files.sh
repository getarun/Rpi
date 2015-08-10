#!/bin/bash
##################
#echo "Use this to Copy Lokal Git Repo in RPi to SD"
#echo "Only use with working versions annotated with tags >= v1.0"
##################

echo "update-local-files: source: /home/pi/git-working-dir/RPi"
echo "Copying data.php, create-graph.html, about.php to webserver (/var/www)"
sudo cp about.php data.php index.html get-watering.php /var/www
echo "chown www-data:www-data to /var/www"
sudo chown www-data:www-data /var/www

echo("Copying control.py to local bin-tree (/usr/bin)")
sudo cp control.py /usr/bin

echo "Setting execution bit to /usr/bin/control.py"
sudo chmod +x /usr/bin/control.py

###installs manpage
echo "Installing man-page to /usr/local/share/man/man1"
install -g 0 -o 0 -m 0644 manpage.1 /usr/local/share/man/man1/control.py.1
gzip /usr/local/shre/man/man1/control.py.1
echo "updating man-page database"
sudo mandb #updates manual pages
