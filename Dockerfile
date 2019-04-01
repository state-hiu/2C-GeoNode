FROM python:2.7.14-stretch
MAINTAINER GeoNode development team

RUN mkdir -p /usr/src/sc

WORKDIR /usr

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		postgresql-client libpq-dev \
		sqlite3 \
                python-gdal python-psycopg2 \
                python-imaging python-lxml \
                python-dev libgdal-dev \
                python-ldap \
                libmemcached-dev libsasl2-dev zlib1g-dev \
                python-pylibmc \
                uwsgi uwsgi-plugin-python \
                vim htop git \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

# python-gdal does not work, let's replace it by pygdal
RUN GDAL_VERSION=`gdal-config --version` \
    && PYGDAL_VERSION="$(pip install pygdal==$GDAL_VERSION 2>&1 | grep -oP '(?<=: )(.*)(?=\))' | grep -oh $GDAL_VERSION\.[0-9])" \
    && pip install pygdal==$PYGDAL_VERSION

# fix for known bug in system-wide packages
RUN ln -fs /usr/lib/python2.7/plat-x86_64-linux-gnu/_sysconfigdata*.py /usr/lib/python2.7/

RUN pip install pipenv
COPY Pipfile /usr/
COPY Pipfile.lock /usr/
RUN pipenv install --system

# This should be close to the last step in order to avoid rebuilding image during development.
COPY . /usr/src/sc
WORKDIR /usr/src/sc

# Patch if needed from the patches folder
RUN cd /usr/local/lib/python2.7/site-packages; \
    for i in /usr/src/sc/patches/*.patch; do patch -p1 < $i; done

# Patch geonode if needed
RUN cd /usr/src/geonode; \
    for i in /usr/src/sc/patches/geonode/*.patch; do patch -p1 < $i; done

ENTRYPOINT ["/usr/src/sc/entrypoint.sh"]
