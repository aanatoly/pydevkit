
SHELL := /bin/bash
PYTHON ?= python3

NAME := $(shell $(PYTHON) setup.py --name | sed 's/-/_/g')
VER := $(shell $(PYTHON) setup.py --version)
PY2 :=
PKG := dist/$(NAME)-$(VER)-$(if $(PY2),py2.)py3-none-any.whl

# Virtual Env, one per OS to avoid mess
slug = $(shell $(1) |& sed -e 's/ /-/g' | tr '[:upper:]' '[:lower:]')
env_distro = $(call slug,lsb_release -ds)
env_python = $(call slug,$(PYTHON) --version)
env_py = $(shell $(PYTHON) --version |& sed -e 's/.*\s/python/' -e 's/\.[^.]\+$$//')
env_path = venv/$(env_distro)/$(env_python)
env_activate = $(env_path)/bin/activate
env_init = $(env_path)/.dev-init
$(info virtualenv: $(env_path))

ENVON = . $(env_activate)

.PHONY: init build install clean distclean test upload
.DEFAULT_GOAL := build

$(env_activate):
	virtualenv -p $(env_py) $(env_path)

all: $(env_activate)

init: $(env_init)
$(env_init): $(env_activate)
	$(ENVON); \
	pip install .[dev]
	touch $@

build: $(PKG)
	@true

$(PKG): $(env_init)
	$(ENVON); \
	python setup.py bdist_wheel $(if $(PY2),--universal)
	ls -al dist

install: $(env_init) $(PKG)
	$(ENVON); \
	pip install $(PKG)
	mkdir -p artifacts; cp dist/*.whl artifacts

clean:
	$(ENVON); \
	pip uninstall -y $(NAME) || true
	rm -rf .eggs build/ dist/ $(NAME).egg-info  */*.pyc

distclean: clean
	rm -rf venv .tox

test: $(env_init)
	$(ENVON); \
	tox -v

upload:
	$(ENVON); \
	twine upload \
		$(if $(PYPI_URL), --repository-url $(PYPI_URL)) \
		$(if $(PYPI_REPO), -r $(PYPI_REPO)) \
		$(PKG)
