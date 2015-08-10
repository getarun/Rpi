#!/bin/bash
cd /home/pi/git-working-dir/RPi

echo "cp data.php, create-graph.html, about.php to /var/www"
sudo cp data.php /var/www
sudo cp create-graph.html /var/www
sudo cp about.php /var/www
echo "chown www-data:www-data to /var/www"
sudo chown www-data:www-data /var/www

echo "Installing control.py to /usr/bin"
sudo cp control.py /usr/bin
echo "Setting execution bit to /usr/bin/control.py"
sudo chmod +x /usr/bin/control.py

###installs manpage
echo "Installing man-page"
gzip manpage.1
sudo cp manpage.1.gz /usr/share/man/
