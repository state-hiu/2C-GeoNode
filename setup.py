import os
from distutils.core import setup

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="state_2c_geonode",
    version="0.1",
    author="",
    author_email="",
    description="state_2c_geonode, based on GeoNode",
    long_description=(read('README.md')),
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
    license="BSD",
    keywords="state_2c_geonode geonode django",
    url='https://github.com/state_2c_geonode/state_2c_geonode',
    packages=['state_2c_geonode',],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
)
