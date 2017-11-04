#!/usr/bin/env python3

from setuptools import setup


with open('README.rst') as fh:
    long_description = fh.read()

setup(
    name='tacl-catalogue-manager',
    version='1.0.0',
    description='Manager for creating TACL catalogue files',
    long_description=long_description,
    author='Jamie Norrish',
    author_email='jamie@artefact.org.nz',
    url='https://github.com/ajenhl/tacl-catalogue-manager',
    packages=['tcm'],
    entry_points={
        'console_scripts': [
            'tcm=tcm.command:main',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
)
