
SHELL := /bin/bash
PYTHON ?= python3

# Virtual Env, one per OS to avoid mess
slug = $(shell $(1) |& sed -e 's/ /-/g' | tr '[:upper:]' '[:lower:]')
env_distro = $(call slug,lsb_release -ds)
env_python = $(call slug,$(PYTHON) --version)

define penv
PE_$(1) = .venv/$(env_distro)/$(env_python)-$(1)
PE_$(1)_BIN = $$(PE_$(1))/bin
PE_$(1)_ON = $$(PE_$(1))/bin/activate
PE_$(1)_ENV = . $$(PE_$(1))/bin/activate
PE_$(1)_INIT = $$(PE_$(1))/bin/activate

init: $$(PE_$(1)_INIT)
$$(PE_$(1)_INIT):
	.ci/mk-venv $(PYTHON) $$(PE_$(1)) $(2)
endef

$(eval $(call penv,APP,-r req-app.txt))
$(eval $(call penv,DEV,build pdm pdm.pep517 setuptools_scm[toml] tox))


.PHONY: init build install einstall clean distclean test upload
.DEFAULT_GOAL := build


init:
	@true

build: $(PE_DEV_INIT)
	rm -rf dist/ build/
	$(PE_DEV_ENV); python -m build -w
	ls -Al dist

# XXX: you can put custom wheels to wheels/
einstall: $(PE_APP_INIT)
	$(PE_APP_ENV); \
	pip install -f wheels/ -e .

install: $(PE_APP_INIT)
	$(PE_APP_ENV); \
	pip install -f wheels/ dist/*.whl

clean:
	rm -rf build/ dist/ .venv

distclean: clean
	rm -rf cache wheels

test: $(PE_DEV_INIT)
	$(PE_DEV_ENV); \
	tox -v $(if $(TOX_ENV),-e $(TOX_ENV))

upload: $(PE_DEV_INIT)
	$(MAKE) build
	$(PE_DEV_ENV); \
	pdm publish --no-build -vv $(if $(PYPI_REPO), -r $(PYPI_REPO))
