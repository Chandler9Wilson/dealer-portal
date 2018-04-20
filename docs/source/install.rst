Installing the project
======================

System Requirements
-------------------

* Debian flavor of linux (tested on Ubuntu 16.04)
* A non root user with ``sudo`` privileges
* Node v.8

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