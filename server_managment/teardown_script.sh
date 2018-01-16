#!/bin/bash
# Made to teardown users and db created with setup_script

echo WARNING this will delete the databases catalog and chandler and their users

# Deletes db and user chandler
sudo -u postgres dropdb -i chandler
sudo -u postgres dropuser -i chandler

# Deletes db acmonitor and user catalog
sudo -u postgres dropdb -i acmonitor
sudo -u postgres dropuser -i catalog