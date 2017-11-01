CREATE DATABASE acmonitor;
CREATE USER catalog WITH PASSWORD 'catalog';
GRANT ALL PRIVILEGES ON DATABASE acmonitor TO catalog;

# /q
# psql -d acmonitor