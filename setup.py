# coding=utf-8
import os
import sys

from setuptools import find_packages
from setuptools import setup

assert sys.version_info[0] == 3 and sys.version_info[1] >= 6, "eosapi requires Python 3.6 or newer."


def readme_file():
    return 'README.rst' if os.path.exists('README.rst') else 'README.md'


# yapf: disable
setup(
    name='eosapi',
    version='0.0.1',
    description='Python EOS API',
    long_description=open(readme_file()).read(),
    packages=find_packages(exclude=['scripts']),
    setup_requires=['pytest-runner'],
    tests_require=['pytest',
                   'pep8',
                   'pytest-pylint',
                   'yapf',
                   'sphinx',
                   'recommonmark',
                   'sphinxcontrib-restbuilder',
                   'sphinxcontrib-programoutput',
                   'pytest-console-scripts'],

    install_requires=[
        # 'appdirs',
        # 'ecdsa',
        # 'pylibscrypt',
        # 'scrypt',
        # 'pycrypto',
        'urllib3>=1.21.1',
        'certifi',
        # 'ujson',
        # 'w3lib',
        # 'maya',
        'toolz',
        'funcy',
        'prettytable',
    ],
    entry_points={
        'console_scripts': [
            'eospy=eos.cli:legacy',
        ]
    })
