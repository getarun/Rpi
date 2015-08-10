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
echo "Installing man-page to /usr/local/share/man/man1"
install -g 0 -o 0 -m 0644 manpage.1 /usr/local/share/man/man1/control.py.1
gzip /usr/local/shre/man/man1/control.py.1

#gzip manpage.1
#sudo cp manpage.1.gz /usr/local/share/man/
#sudo chmod 0644 /usr/local/share/man/control.1.gz
