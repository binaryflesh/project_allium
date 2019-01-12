from setuptools import setup

with open("README.md") as fp:
    long_description = fp.read()

setup(
    name='allium',
    version='1.0',
    description='ACM Cryptocurrency',
    url='https://github.com/SIGBlockchain/project_allium',
    download_url='https://github.com/SIGBlockchain/project_allium',
    long_description=long_description,
    install_requires=[
        'requests',
        'ecdsa'
    ]
)
