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
  * Allow port 80 tcp for apache

    * ``$ sudo ufw allow www``
  * Allow port 123 for NTP

    * ``$ sudo ufw allow ntp``

Installing needed software
--------------------------

* Install nvm

  * `$ curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash`
* Install node (after session restart)

  * `$ nvm install 8`
* :doc:`install`
* Make sure gunicorn is serving the project correctly

  * Open port 8000 to test

    * ``$ sudo ufw allow 8000/tcp``
  * Run ``$ gunicorn --bind 0.0.0.0:8000 portal_server:app``
  * Close the port if it is working

    * ``$ sudo ufw delete allow 8000/tcp``


Guide Reference
---------------

* relevant man pages
* Used [this](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04) for usermod command and the ssh-copy-id script. I have set up servers before just couldnt remember those two lines.
* A nice walk through the [options with UFW](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04) a little nicer/more concise than the man page.
* I am using the mod_wsgi-express script included with the [mod_wsgi package](https://pypi.python.org/pypi/mod_wsgi)