#!/bin/bash
cd /home/pi/git-working-dir/RPi

sudo cp data.php /var/www
sudo cp create-graph.html /var/www
sudo cp control.py /usr/bin
sudo cp about.php /var/www

sudo chmod +x /usr/bin/control.py

sudo chown www-data:www-data /var/www

###installs manpage
echo "installing man-page"
gzip manpage.1
sudo cp manpage.1.gz /usr/share/man/
