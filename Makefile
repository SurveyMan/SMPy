smpyversion = $(cat VERSION)
projectdir = $(shell pwd)

# this line clears ridiculous number of default rules
.SUFFIXES:
.PHONY : deps test package distr

deps :
	pip install numpy
	pip install matplotlib	
	pip install jsonschema

test : deps
	python -m surveyman.test

package :
	python setup.py sdist

distr : package
	python setup.py register
	python setup.py sdist upload
