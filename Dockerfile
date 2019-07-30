FROM python:2.7.16-buster
MAINTAINER GeoNode development team

RUN mkdir -p /usr/src/sc

WORKDIR /usr

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		postgresql-client libpq-dev \
		sqlite3 \
                python-gdal python-psycopg2 \
                python-pil python-lxml \
                python-dev libgdal-dev \
                python-ldap \
                libmemcached-dev libsasl2-dev zlib1g-dev \
                python-pylibmc \
                uwsgi uwsgi-plugin-python \
                vim htop git \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*


# fix for known bug in system-wide packages
RUN ln -fs /usr/lib/python2.7/plat-x86_64-linux-gnu/_sysconfigdata*.py /usr/lib/python2.7/

RUN pip install pipenv
COPY requirements.txt /usr/
RUN pip install -r requirements.txt

# Install pygdal (after requirements for numpy 1.16)
RUN pip install pygdal==$(gdal-config --version).*

# Install GeoNode 2.10x branch as of July 18
RUN pip install --no-deps https://github.com/GeoNode/geonode/archive/fc57782f28ad05f018264808257dd677360b64f7.zip

# Set up the machine to be able to patch deps in site-packages
WORKDIR /usr/local/lib/python2.7/site-packages
RUN git init \
 && git add * \
 && git config --global user.email "<>" \
 && git config --global user.name "sc" \
 && git commit -m "Initial state"

# Copy patches for GeoNode and other dependencies.
COPY patches /usr/src/sc/patches

# Patch GeoNode and other deps if needed from the patches folder
RUN cd /usr/local/lib/python2.7/site-packages; \
    for i in /usr/src/sc/patches/*.patch; do patch -p1 < $i; done

# This should be close to the last step in order to avoid rebuilding image during development.
COPY . /usr/src/sc
WORKDIR /usr/src/sc
RUN python setup.py develop --no-deps

ENTRYPOINT ["/usr/src/sc/entrypoint.sh"]
