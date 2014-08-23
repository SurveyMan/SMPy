smpyversion = $(cat VERSION)
projectdir = $(shell pwd)

# this line clears ridiculous number of default rules
.SUFFIXES:
.PHONY: deps test package distr

deps:
	pip install jsonschema
	pip install pytidylib

test: deps
	pip --version
	pip show jsonschema
	pip show pytidylib
	python -m surveyman.test

package:
	python setup.py sdist

distr: package
	python setup.py register
	python setup.py sdist upload

travis:
	python setup.py install
	python -m surveyman.test
