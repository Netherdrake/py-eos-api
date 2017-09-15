ROOT_DIR := .
DOCS_DIR := $(ROOT_DIR)/docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build


default: install

test: test-without-lint

test-without-lint:
	py.test tests

clean: clean-build clean-pyc

clean-build:
	rm -fr build/ dist/ *.egg-info .eggs/ .tox/ __pycache__/ .cache/ .coverage htmlcov src

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

install: clean
	pip install -e .

pypi:
	python -c "import pypandoc;pypandoc.convert(source='README.md', format='markdown_github', to='rst', outputfile='README.rst')"
	python setup.py bdist_wheel --universal
	python setup.py sdist bdist_wheel upload
	rm README.rst
