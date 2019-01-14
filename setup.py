#!/bin/bash
'''
Run sudo python3 setup.py install
'''

from setuptools import setup, find_packages

with open("README.md") as fp:
    long_description = fp.read()

setup(
    name='allium',
    version='1.0',
    description='ACM Cryptocurrency',
    url='https://github.com/SIGBlockchain/project_allium',
    long_description=long_description,
    install_requires=[
        'requests',
        'ecdsa',
        'pyqt5'
    ],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
