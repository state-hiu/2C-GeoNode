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

RUN cd src && git clone https://github.com/GeoNode/geonode.git 
RUN cd src/geonode && git reset --hard fc57782f28ad05f018264808257dd677360b64f7

RUN pip install -e /usr/src/geonode


# This should be close to the last step in order to avoid rebuilding image during development.
COPY . /usr/src/sc
WORKDIR /usr/src/sc

RUN pip install -e /usr/src/sc 
# Patch if needed from the patches folder
#RUN cd /usr/local/lib/python2.7/site-packages; \
#    for i in /usr/src/sc/patches/*.patch; do patch -p1 < $i; done

# Patch geonode if needed
#RUN cd /usr/src/geonode; \
#    for i in /usr/src/sc/patches/geonode/*.patch; do patch -p1 < $i; done

# Install pygdal (after requirements for numpy 1.16)
RUN pip install pygdal==$(gdal-config --version).*

ENTRYPOINT ["/usr/src/sc/entrypoint.sh"]
