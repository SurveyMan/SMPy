#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup, find_packages

f = open('VERSION', 'r')
v = f.read()
f.close()

setup(
    name='SMPy',
    version=v,
    author='Emma Tosch',
    author_email='etosch@cs.umass.edu',
    packages=['surveyman', 'surveyman.test', 'surveyman.survey'],
    package_data={'': ['*.json']},
    url='http://surveyman.github.io/SMPy',
    license='CRAPL',
    description='Python front-end to the SurveyMan Language and Runtime',
    long_description=open('README.txt').read(),
    install_requires=[
        "jsonschema == 2.3.0",
        "pytidylib ==  0.2.3"
    ],
)
