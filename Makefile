.PHONY: clean-pyc clean-build docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-test:
	rm -fr .tox/

lint:
	flake8 doconv tests

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source doconv setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/doconv.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ doconv
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	xdg-open docs/_build/html/index.html

pre-release: lint
	./pre-release.sh

release: clean
	python setup.py sdist upload

sdist: clean
	python setup.py sdist
	ls -l dist
