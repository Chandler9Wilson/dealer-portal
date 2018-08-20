Running the Project
===================

There are two main ways that the ``portal_server`` project can be run:

Flask's built-in server
-----------------------

Flasks built in development server is useful for its live reload functionality.

* Make sure you are in the virtual env and at the project root
* Start the server with `$ python run.py`

Gunicorn
--------

Gunicorn is the WSGI server used in production but it can also be run on your development machine.

* Make sure you are in the virtual env and at the project root
* Start the server with `$ gunicorn -w 4 portal_server:app`


Configuration
-------------

Runtime configuration works the same way either way you choose to run the project.

* Just set the ``FLASK_CONFIGURATION`` envvar to one of the options found in ``__init__.py``

  * e.g. to set the config to development run: ``$ export FLASK_CONFIGURATION="development"``

If you are having problems with setting up the envvar try these steps

1. Make sure the user you are setting the envvar on is the same one running the project.
2. Try debugging the envvar using some of the commands from `this digital ocean guide`_.

Configuration Options are stored at the ``portal_server`` package root in the ``config.py`` and ``init.py`` files.
For help on understanding these files see `Flask's config docs`_.

.. _`this digital ocean guide`: https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-a-linux-vps
.. _`Flask's config docs`: http://flask.pocoo.org/docs/1.0/config/#development-production