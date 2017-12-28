# this assumes that
'''
CREATE DATABASE acmonitor;
CREATE USER catalog WITH PASSWORD 'catalog';
GRANT ALL PRIVILEGES ON DATABASE acmonitor TO catalog;
'''
# has been run
# also for SELECT privileges https://serverfault.com/a/284278
# TODO improve security for deployment
