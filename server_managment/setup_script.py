#!/usr/bin/env python3
# A setup script for servers or development machines running dealer_portal
# should be run as your dev user, based on
# https://gist.github.com/SteveWooding/a62d04af359c39a08f5fd545cfc3e67d
import os
import subprocess
import sys

# TODO fail if this is not >3.5
print(sys.version)


def install_postgresql():
    # Update the package database
    print('Updating packages....')
    subprocess.run('sudo apt-get -qqy update',
                   stderr=subprocess.PIPE, shell=True)

    print('Attempting install of postgresql.... ')
    subprocess.run(
        'sudo apt-get -qqy install make zip unzip postgresql',
        stderr=subprocess.PIPE, check=True, shell=True)


def start_postresql():
    print('Starting postgresql.... ')
    subprocess.run('sudo service postgresql start',
                   stderr=subprocess.PIPE, check=True, shell=True)


def create_dbs():
    # Create a PostgreSQL user for the current Linux user and
    # create a db in their name
    subprocess.run('sudo - u postgres createuser - dRS $USER && createdb',
                   stderr=subprocess.PIPE, shell=True)

    # Create the catalog PostgreSQL user
    print('-' * 30)
    print('Creating the catalog PostgreSQL user. Set password to catalog')
    print('-' * 30)
    subprocess.run('sudo -u postgres createuser -dRSP catalog',
                   stderr=subprocess.PIPE, check=True, shell=True)

    # Create the catalog database with catalog as the owner
    subprocess.run('sudo -u postgres createdb -O catalog acmonitor',
                   stderr=subprocess.PIPE, check=True, shell=True)


def setup_venv(script_path):
    # script_path should be the path to catalog/server_managment/

    # Changes the scripts working directory so relative paths work
    os.chdir(script_path)

    print('Installing venv package')
    subprocess.run('sudo apt-get python3-venv',
                   stderr=subprocess.PIPE, check=True, shell=True)

    print('Creating virtual environment')
    subprocess.run('python3 -m venv ../env',
                   stderr=subprocess.PIPE, check=True, shell=True)

    print('Installing requirments.txt in the virtual environment')
    subprocess.run('../env/bin/pip install -r ../requirements.txt',
                   stderr=subprocess.PIPE, check=True, shell=True)


def setup_models(script_path):
    # script_path should be the path to catalog/server_managment/
    # TODO add code so that setup.py and
    # based on user input import_fake_data.py are run automattically
    print('Please run ./setup.py in the venv from ./ ' +
          'with `$ python -m db.setup` to setup db.models && if you' +
          'need fake data run ./db/import_fake_data.py')

    # Changes the scripts working directory so relative paths work
    ''' os.chdir(script_path)

    subprocess.run('../env/bin/python -m ../db/setup',
                   stderr=subprocess.PIPE, check=True, shell=True) '''


def interactive():
    script_path = sys.path[0]

    print('-' * 30)
    print('Is this a first time setup of the project? (Y/n)')
    print('-' * 30)
    answer = input()

    if answer in ('Y', 'y'):
        install_postgresql()
        start_postresql()
        create_dbs()
        setup_venv(script_path)
        setup_models(script_path)
    elif answer in ('N', 'n'):
        start_postresql()
        create_dbs()
    elif answer in ('Test', 'test'):
        setup_models(script_path)
    else:
        print('Please enter a valid answer (Y/n)')
        interactive()


if __name__ == '__main__':
    interactive()
