## Development

Build package
```sh
make build
make test
```

Local (editable) install
```sh
make einstall
```

Run dev tool
```sh
.ci/venv --name=dev run flake8 src/
```

Run app script, as defined in pyproject.toml
```sh
.ci/venv --name=app run script
```

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
.ci/venv run pre-commit install
```

Or if you want them to run only for each push:

```sh
.ci/venv run pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
.ci/venv run pre-commit run --all-files
```

### Update build scripts
This project was generated using the [pdk-cookiecutter](https://github.com/aanatoly/pdk-cookiecutter) template.
You can always update build scripts boilerplate by running
```sh
.ci/venv run cruft update
```
