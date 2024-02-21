# make me a generic setup.py file for a package named baseflow, version 0.0.1

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='baseflow',
    version='0.0.1',
    packages=find_packages(),
    install_requires=install_requires
)
