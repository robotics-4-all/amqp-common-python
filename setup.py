#!/usr/bin/env python

import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now
#   1) we have a top level README file
#   2) it's easier to type in the README file than to put a raw string in below
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    install_requires=read('requirements.txt').splitlines(),
    name='amqp_common',
    version='0.8.9',
    description=
        'RPC and PubSub implementation in python over AMQP.' +
        'Thin wrapper arround Pika',
    url='https://github.com/robotics-4-all/amqp-common-python/',
    download_url='',
    author='Konstantinos Panayiotou',
    author_email='klpanagi@gmail.com',
    maintainer='Konstantinos Panayiotou',
    maintainer_email='klpanagi@gmail.com',
    license='Apache 2',
    test_suite='tests',
    include_package_data=True,
    # A list naming all the packages you want to include
    packages=find_packages(),
    # Package data to be added to packages
    package_data={},
    # Specify additional files needed by the module distribution:
    #  configuration files, message catalogs, data files
    data_files=[],
    # A script(s) to be installed into standard locations like /usr/bin
    scripts=[],
    zip_safe=True,
    long_description=read('README.md') if os.path.exists('README.md') else "")
