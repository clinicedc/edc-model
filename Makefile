all: init docs clean test

env:
	pip install pytest pytest-cov flake8 coverage black

clean: clean-build clean-pyc
	rm -fr htmlcov/

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

init:
	pip install "tox>=1.8" coverage Sphinx

test:
	coverage erase
	tox
	coverage html

docs: documentation

documentation:
	sphinx-build -b html -d docs/_build/doctrees docs docs/_build/html

dist: clean
	pip install -U wheel
	python setup.py sdist
	python setup.py bdist_wheel
	for file in dist/* ; do gpg --detach-sign -a "$$file" ; done
	ls -l dist

test-release: dist
	pip install -U twine
	gpg --detach-sign -a dist/*
	twine upload -r testpypi dist/*

release: dist
	pip install -U twine
	gpg --detach-sign -a dist/*
	twine upload dist/*

format:
	black edc_model
