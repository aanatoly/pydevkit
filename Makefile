
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := init
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
export PYTHON ?= python3

define penv
env_$(1) = .ci/venv --name=$(1) run
env_$(1)_dir = $$(shell .ci/venv --name=$(1) dir)

init: $$(env_$(1)_dir)
$$(env_$(1)_dir):
	.ci/venv --name=$(1) init
ifneq ($(2),)
	.ci/venv --name=$(1) run pip install -f wheels/ $(2)
endif
endef

$(eval $(call penv,app,))
$(eval $(call penv,dev,-r .ci/requirements.txt))


.PHONY: init build install einstall clean distclean test upload

init:
	@true

build: $(env_dev_dir)
	rm -rf dist/ build/
	$(env_dev) python -m build -w
	ls -Al dist

# XXX: you can put custom wheels to wheels/
einstall: $(env_app_dir)
	$(env_app) pip install -f wheels/ -e .

install: $(env_app_dir)
	$(env_app) pip install -f wheels/ dist/*.whl

clean:
	rm -rf build/ dist/ .venv

distclean: clean
	rm -rf cache wheels

test: $(env_dev_dir)
	$(env_dev) tox -v $(if $(TOX_ENV),-e $(TOX_ENV))

lint: $(env_dev_dir)
	$(env_dev) pre-commit run $(if $(V),-v)

lint-all: $(env_dev_dir)
	$(env_dev) pre-commit run --all-files $(if $(V),-v)

upload: $(env_dev_dir)
	$(MAKE) build
	$(env_dev) pdm publish --no-build -vv $(if $(PYPI_REPO), -r $(PYPI_REPO))
