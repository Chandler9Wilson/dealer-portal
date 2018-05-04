Installing the project
======================

System Requirements
-------------------

* Debian flavor of linux (tested on Ubuntu 16.04)
* A non root user with ``sudo`` privileges
* Node v.8

Create a secrets.py file
------------------------

A secrets.py file is used to store several things. **This file needs to be restricted in production environments** using `chmod`_.

The file needs to contains the following:

* Database username and password

  * Both should be set during the ``setup_script``.
    Make sure you have the same credentials copied over (username's default is ``catalog``) or the application will not work.
* Flask's ``secret_key`` which is used for session cryptography

  * To generate a good key run ``$ python -c 'import os; print(os.urandom(16))'``

An example ``secrets.py`` file would be as follows:

.. code-block:: python

    db_username = 'catalog'
    db_password = 'catalog'
    flask_secret_key = b'\xfa\x85\xf7\xcc/I\xb7\xf2\xa1P\xb0o\xae\x95s\x17'

.. _`chmod`: https://www.computerhope.com/unix/uchmod.htm

Install Steps
-------------

* First time setup (This project has to be run in a debian based environment)

  1. **All commands should be run from the project root unless a cd command was instructed previously**
  2. Run ``$ ./server_management/setup_script.py`` respond yes when prompted if this is your first time.
  3. Run ``$ source env/bin/activate``
  4. Run ``$ python -m portal_server.db.setup``
  5. If you want fake data in your db run ``$ python -m portal_server.db.import_fake_data``
  6. ``$ cd portal_server/directory/home_static``
  7. Run ``$ npm install``
  8. Run ``$ npm run dev-build``
  9. Return to project root ``$ cd ../../..``
  10. Run ``$ python run.py``
  11. Visit the `login page`__

.. _login: http://localhost:8000/login/
__ login_