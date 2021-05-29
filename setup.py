# python3 setup.py sdist
# https://docs.python.org/3/distutils/sourcedist.html
# pip3 install https://github.com/CrashCash/ZeroServer/raw/master/dist/zeroserver-1.0.tar.gz
#
from setuptools import find_packages, setup
desc="""\
ZeroServer
==========
A small website using Flask to monitor a Zero electric motorcycle while it's charging.
"""

setup(
    author='Gene Cash',
    author_email='genecash@fastmail.com',
    url='https://github.com/CrashCash/ZeroServer',
    name='zeroserver',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', 'gunicorn', 'zerobt'],
    dependency_links=['https://github.com/CrashCash/ZeroBT/raw/master/dist/zerobt-1.0.tar.gz'],
)
