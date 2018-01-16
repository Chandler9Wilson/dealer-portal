#!/bin/bash
# A setup script for servers or development machines running dealer_portal should be run as your dev user
# based on https://gist.github.com/SteveWooding/a62d04af359c39a08f5fd545cfc3e67d

# Update the Ubuntu package database
sudo apt-get -qqy update

sudo apt-get -qqy install make zip unzip postgresql

# Make sure that PostgreSQL is running
sudo service postgresql start

# Create a PostgreSQL user for the current Linux user
sudo -u postgres createuser -dRS $USER
# Creates a db named the same as $USER
createdb

# Create the vagrant PostgreSQL user
echo "#######################################################################################"
echo "# Creating the vagrant PostgreSQL user. Set password to \"catalog\" (without quotes)... #"
echo "#######################################################################################"
sudo -u postgres createuser -dRSP catalog

# Create the news database and have it owned by the vagrant PostgreSQL user
sudo -u postgres createdb -O catalog acmonitor

python ./db/setup_models.py
