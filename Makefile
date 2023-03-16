
SHELL := /bin/bash
export PYTHON ?= python3

define penv
env_$(1) = .ci/venv --name=$(1) run
env_$(1)_dir = $$(shell .ci/venv --name=$(1) dir)

init: $$(env_$(1)_dir)
$$(env_$(1)_dir):
	.ci/venv --name=$(1) init $(2)
endef

$(eval $(call penv,app,))
$(eval $(call penv,dev,-r .ci/requirements.txt))


.PHONY: init build install einstall clean distclean test upload
.DEFAULT_GOAL := build

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

upload: $(env_dev_dir)
	$(MAKE) build
	$(env_dev) pdm publish --no-build -vv $(if $(PYPI_REPO), -r $(PYPI_REPO))
