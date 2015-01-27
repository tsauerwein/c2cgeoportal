#!/bin/bash -e

cp travis/build.mk /tmp/test/travis.mk

cd /tmp/test/
mkdir print/print-app

git config --global user.name "Travis"
git config --global user.email "travis@example.com"
git init
git add -A
git submodule add https://github.com/camptocamp/cgxp.git test/static/lib/cgxp
git commit -m "Initial commit"

sudo chmod 777 /var/lib/tomcat7/webapps

make -f travis.mk build

echo "Build complete"

sudo -u postgres psql -d geomapfish -c "CREATE SCHEMA main;"
.build/venv/bin/alembic upgrade head

sudo touch /etc/apache2/sites-enabled/test.conf
sudo chmod 666 /etc/apache2/sites-enabled/test.conf
echo "Include /tmp/test/apache/*.conf" > /etc/apache2/sites-enabled/test.conf

sudo a2enmod headers
sudo a2enmod rewrite
sudo a2enmod wsgi
sudo /usr/sbin/apachectl restart

cd -
