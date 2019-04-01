Sc
========================

GeoNode template project. Generates a django project with GeoNode support.

Developer Workshop
------------------

Available at::

    http://geonode.org/dev-workshop


Create a custom project
-----------------------

Note: You can call your geonode project whatever you like following the naming conventions for python packages (generally lower case with underscores (``_``). In the examples below, replace ``my_geonode`` with whatever you would like to name your project.

Using a Python virtual environment
++++++++++++++++++++++++++++++++++

To setup your project using a local python virtual environment, follow these instructions:

1. Prepare the Environment

  .. code:: bash

    git clone https://github.com/GeoNode/geonode-project.git -b master
    mkvirtualenv my_geonode
    pip install Django==1.11.16

    django-admin startproject --template=./geonode-project -e py,rst,json,yml,ini,env,sample -n Dockerfile my_geonode

    cd my_geonode

2. Setup the Python Dependencies

  .. code:: bash

    pip install -r requirements.txt --upgrade
    pip install -e . --upgrade

    GDAL_VERSION=`gdal-config --version`
    PYGDAL_VERSION="$(pip install pygdal==$GDAL_VERSION 2>&1 | grep -oP '(?<=: )(.*)(?=\))' | grep -oh $GDAL_VERSION\.[0-9])"
    pip install pygdal==$PYGDAL_VERSION

    # Using Default Settings
    DJANGO_SETTINGS_MODULE=my_geonode.settings paver reset
    DJANGO_SETTINGS_MODULE=my_geonode.settings paver setup
    DJANGO_SETTINGS_MODULE=my_geonode.settings paver sync
    DJANGO_SETTINGS_MODULE=my_geonode.settings paver start

    # Using Custom Local Settings
    cp my_geonode/local_settings.py.sample my_geonode/local_settings.py

    vim my_geonode/wsgi.py
    --> os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_geonode.local_settings")

    DJANGO_SETTINGS_MODULE=my_geonode.local_settings paver reset
    DJANGO_SETTINGS_MODULE=my_geonode.local_settings paver setup
    DJANGO_SETTINGS_MODULE=my_geonode.local_settings paver sync
    DJANGO_SETTINGS_MODULE=my_geonode.local_settings paver start

3. Access GeoNode from browser::

    http://localhost:8000/

.. note:: default admin user is ``admin`` (with pw: ``admin``)

Start your server
-----------------

You need Docker 1.12 or higher, get the latest stable official release for your platform.

1. Prepare the Environment

  .. code:: bash

    git clone https://github.com/GeoNode/geonode-project.git -b master
    mkvirtualenv my_geonode
    pip install Django==1.11.16

    django-admin startproject --template=./geonode-project -e py,rst,json,yml,ini,env,sample -n Dockerfile my_geonode

    cd my_geonode

2. Run `docker-compose` to start it up (get a cup of coffee or tea while you wait)

   Remember to update "wsgi.py" in case you are using "local_settings"
   vim my_geonode/wsgi.py
   --> os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_geonode.local_settings")

   .. code:: bash

     docker-compose build --no-cache
     docker-compose up -d
   
   .. code-block:: none
   
      set COMPOSE_CONVERT_WINDOWS_PATHS=1 
   
   before running docker-compose up

3. Access the site on http://localhost/


If you want to run the instance on a public site
------------------------------------------------

Preparation of the image (First time only)
++++++++++++++++++++++++++++++++++++++++++

.. note:: In this example we are going to publish to the public IP http://123.456.789.111

.. code:: bash

  vim docker-compose.override.yml
    --> replace localhost with 123.456.789.111 everywhere

Startup the image
+++++++++++++++++

.. code:: bash

  docker-compose up --build -d


To Stop the Docker Images
-------------------------

.. code:: bash

  docker-compose stop


To Fully Wipe-out the Docker Images
-----------------------------------

.. warning:: This will wipe out all the repositories created until now.

.. note:: The images must be stopped first

.. code:: bash

  docker system prune -a


Recommended: Track your changes
-------------------------------

Step 1. Install Git (for Linux, Mac or Windows).

Step 2. Init git locally and do the first commit:

    git init

    git add *

    git commit -m "Initial Commit"

Step 3. Set up a free account on github or bitbucket and make a copy of the repo there.

Hints: Configuring Requirements.txt
-----------------------------------

You may want to configure your requirements.txt, if you are using additional or custom versions of python packages.  For example::

    Django==1.11.16
    six==1.10.0
    django-cuser==2017.3.16
    django-model-utils==3.1.1
    pyshp==1.2.12
    celery==4.1.0
    Shapely>=1.5.13,<1.6.dev0
    proj==0.1.0
    pyproj==1.9.5.1
    pygdal==2.2.1.3
    inflection==0.3.1
    git+git://github.com/<your organization>/geonode.git@<your branch>


Hints: Using Ansible
--------------------

You will need to use Ansible Role in order to run the playbook.

In order to install and setup Ansible, run the following commands::

    sudo apt-get install software-properties-common
    sudo apt-add-repository ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install ansible

A sample Ansible Role can be found at https://github.com/GeoNode/ansible-geonode

To install the default one, run::

    sudo ansible-galaxy install GeoNode.geonode

you will find the Ansible files into the ``~/.ansible/roles`` folder. Those must be updated in order to match the GeoNode and GeoServer versions you will need to install.

To run the Ansible playbook use something like this::

    ANSIBLE_ROLES_PATH=~.ansible/roles ansible-playbook -e "gs_root_password=<new gs root password>" -e "gs_admin_password=<new gs admin password>" -e "dj_superuser_password=<new django admin password>" -i inventory --limit all playbook.yml


Configuration
=============

Since this application uses geonode, base source of settings is ``geonode.settings`` module. It provides defaults for many items, which are used by geonode. This application has own settings module, ``sc.settings``, which includes ``geonode.settings``. It customizes few elements:
 * static/media files locations - they will be collected and stored along with this application files by default. This is useful during development.
 * Adds ``sc`` to installed applications, updates templates, staticfiles dirs, sets urlconf to ``sc.urls``.

Whether you deploy development or production environment, you should create additional settings file. Convention is to make ``sc.local_settings`` module. It is recommended to use ``sc/local_settings.py``.. That file contains small subset of settings for edition. It should:
 * not be versioned along with application (because changes you make for your private deployment may become public),
 * have customized at least ``DATABASES``, ``SECRET_KEY`` and ``SITEURL``.

You can add more settings there, note however, some settings (notably ``DEBUG_STATIC``, ``EMAIL_ENABLE``, ``*_ROOT``, and few others) can be used by other settings, or as condition values, which change other settings. For example, ``EMAIL_ENABLE`` defined in ``geonode.settings`` enables whole email handling block, so if you disable it in your ``local_settings``, derived settings will be preserved. You should carefully check if additional settings you change don't trigger other settings.

To illustrate whole concept of chained settings:
::
    +------------------------+-------------+-------------------------------+-------------+----------------------------------+
    |  GeoNode configuration |             |   Your application default    |             |  (optionally) Your deployment(s) |
    |                        |             |        configuration          |             |                                  |
    +========================|=============|===============================|=============|==================================+
    |                        | included by |                               | included by |                                  |
    |   geonode.settings     |     ->      |  sc.settings    |      ->     |  sc.local_settings |
    +------------------------|-------------|-------------------------------|-------------|----------------------------------+

Reproducing
===========

#1. Install docker and docker-compose

#2. Download the geonode template folder:

```
wget https://github.com/geonode/geonode-project/archive/master.zip
```

#3. Create the custom geonode project using a volatile docker container:

```
docker run --interactive --tty --rm --user "$(id -u):$(id -g)" --volume "$PWD":/usr/src/app --workdir /usr/src/app rvernica/django django-admin.py startproject --template=master.zip -e py,rst,json,yml,ini,env,sample -n Dockerfile sc 
```

#4. Replace localhost mentions with your server in docker-compose.override.yml and replace them with mydomain.com, make sure you add an entry in your /etc/hosts file for mydomain.com resolving to your box if you have not purchased the domain.

#5. Run docker-compose up to get a server on port 80

```
docker-compose up -d
```

#6. Buy a new dns and point the wildcard at the server's ip address

#7. Get an SSL certificate via certbot:

```
certbot certonly --manual -d mydomain.com --agree-tos --manual-public-ip-logging-ok --preferred-challenges dns-01 --server https://acme-v02.api.letsencrypt.org/directory --config-dir crt --work-dir crt --logs-dir crt
```

#8. Run nginx on port 443 to proxy 

```
  events {
    worker_connections  4096;
  }

  http {
    include       ${pkgs.nginx}/conf/mime.types;
    default_type  application/octet-stream;
  
    server {
      listen 443 ssl http2;
      server_name mydomain.com;
      ssl_certificate /var/lib/acme/wild/live/mydomain/fullchain.pem;
      ssl_certificate_key /var/lib/acme/wild/live/mydomain/privkey.pem;
      add_header Strict-Transport-Security "max-age=15768000; includeSubDomains" always;
    
      ssl_protocols TLSv1.2 TLSv1.3;
      ssl_prefer_server_ciphers on;
      ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+aRSA+SHA384 !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";
      ssl_session_cache shared:ssl_session_cache:10m;


      location / {
        root /d/puerti.co/;
        proxy_set_header Host $host;
        proxy_pass http://mydomain.com/;
      }

   }
  }

```


Loading only data

Step 1. Get raster data from geoserver data dir, mount the volume on a docker container and use importlayers on the folder (OK)
Step 2. Get vector data from the postgres data dump, mount the volume on the django container and run pg_restore (OK)
Step 3. Dump list of layer names from postgres into a csv
Step 4. Create layers using the names in the csv file
Step 5. Write a script that matches tables in the database with tables in django and creates geoserver entries.
