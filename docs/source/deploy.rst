Deploying the Project
=====================

Setting up the server
---------------------

* Changes made to /etc/ssh/sshd_config

  * ``Port 2200``
  * ``PermitRootLogin no``
  * ``PasswordAuthentication no``

* UFW config

  * Allow port 2200 tcp for alternate SSH port

    * ``$ sudo ufw allow 2200/tcp``
  * Allow port nginx

    * ``$ sudo ufw allow 'Nginx Full'``
  * Allow port 123 for NTP

    * ``$ sudo ufw allow ntp``

Installing needed software
--------------------------

* Install nvm

  * ``$ curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash``
* Install node (after session restart)

  * ``$ nvm install 8``
* Install nginx

  * ``$ sudo apt-get install nginx``
* :doc:`install`
* Make sure gunicorn is serving the project correctly

  * Open port 8000 to test

    * ``$ sudo ufw allow 8000/tcp``
  * Run ``$ gunicorn --bind 0.0.0.0:8000 portal_server:app``
  * Close the port if it is working

    * ``$ sudo ufw delete allow 8000/tcp``


Setup systemd service
---------------------

* You should follow the instructions in `this tutorial`_
* The contents of ``/etc/systemd/system/dealer-portal.service`` should be as follows except with an updated user

.. code-block:: guess

    [Unit]
    Description=Gunicorn instance to serve dealer-portal
    After=network.target

    [Service]
    User=chandler
    Group=www-data
    WorkingDirectory=/home/chandler/dealer-portal
    Environment="Path=/home/chandler/dealer-portal/env/bin"
    ExecStart=/home/chandler/dealer-portal/env/bin/gunicorn --workers 3 --bind unix:dealer-portal.sock -m 007 portal_server:app

    [Install]
    WantedBy=multi-user.target


.. _`this tutorial`: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04#create-a-systemd-unit-file

Configure Nginx
---------------

* You should follow the instructions in `this config tutorial`_
* The contents of ``/etc/nginx/sites-available/dealer-portal`` should be as follows except with an updated user

.. code-block:: guess

    server {
        listen 80;
        server_name chandler9wilson.com;

        location / {
            include proxy_params;
            proxy_pass http://unix:/home/chandler/dealer-portal/dealer-portal.sock;
        }
    }


.. _`this config tutorial`: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04#configuring-nginx-to-proxy-requests


Updating Content
----------------

From the project root run the following

1. Run ``$ git pull``
2. Rebuild webpack if needed

  * ``$ cd portal_server/directory/home_static``
  * ``$ npm run build``

3. ``$ sudo systemctl restart dealer-portal``
4. ``$ sudo systemctl restart nginx``


Improvements to be made
-----------------------

Currently static content is large and served relativly slowling through flask. This can be fixed by serving through nginx and gziping in or after the build.

* `Change headers for gzip`_
* `Serve Static content through Nginx`_

.. _`Change headers for gzip`: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding
.. _`Serve Static content through Nginx`: http://docs.gunicorn.org/en/latest/deploy.html

Guide Reference
---------------

* relevant man pages
* Used [this](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04) for usermod command and the ssh-copy-id script. I have set up servers before just couldnt remember those two lines.
* A nice walk through the [options with UFW](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04) a little nicer/more concise than the man page.
* Overall I am using `this guide`_ for setting up nginx and gunicorn

.. _`this guide`: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04