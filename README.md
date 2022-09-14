# pydevkit
Welcome to Python Development Kit.

It provides functionality, frequently needed in a python develpment:
 * logging
    * 4 predefined configurations (incl json logs)
    * control via command-line
    * control via environment variables
 * colors
    * ANSI coloration with command-line control
 * shell
    * printf-like shell command wrapper
 * argparse
    * environment-aware options with lookup order
      command line `>` environemnt `>` default
    * use module doc string as a help message
    * help formatter with switchable default and source var sections

To install it, run
```bash
pip3 install pydevkit
```

## Logging

Out-of-the-box logging configuration.<br>

![Alt text](doc/log.png "a title")


#### Usage
Add this line to the entrypoint.
```python
import pydevkit.log.config  # noqa: F401
from pydevkit.argparse import ArgumentParser

def get_args():
    p = ArgumentParser(help=__doc__, version='1.2.3')
```

No need to modify any other code. It should use standard `logging` module.

```python
import logging
log = logging.getLogger(__name__)
```
#### Run-time options

Now you can use both `PYDEVKIT_LOG_` environment variables and `--log-`
comand-line options. For example:
```bash
PYDEVKIT_LOG_HANDLER=app ./script --log-level=debug
```
Here is the list of all logging options:
 * level - `debug`, `info`, `warning`, `error`, `critical`
 * handler - `app`, `app_mini`, `json`, `json_mini`
 * date -  `datetime`, `date`, `time` or strftime format eg `%Y-%m-%d`
 * color - `auto`, `yes`, `no`. If `auto` is selected, module will enable coloration
   for terminals and disable when output is redirected to pipe or file.
 * threads - `yes`, `no`. Include thread name in a log


#### Developer info
You can pass extra args to the logger with
```python
log.info("main text", extra={"extra": {"more": "info"}})
```

#### Exrternal configuration
If `PYTHON_LOGGING_CONFIG` variable is defined and points to a file, PDK will
use it to configure standard `logging` module, using `dictConfig` (for json files)
or `fileConfig` methods.


## Argparse
Custom ArgParse wrapper featuring
 * derive help from documentation
 * auto-detect application name
 * add logging options

### Usage
Add to the entrypoint
```python
from pydevkit.argparse import ArgumentParser

def main():
    p = ArgumentParser(_help=__doc__)
    # FIXME: add args here
    # p.add_argument("--my-arg")
    Args, UnknownArgs = p.args_resolve()

```

### Add logging options
Provided `ArgParser` has all logging options and upon resolve will automatically
configure logging

### Derive help from documentation
This feature allows you to use single string, usually main `__doc__`string, to
initialize `ArgParser`. Add documentation string to the entrypoint

```python
#!/usr/bin/env python
'''
Main help message
and another line

EPILOG:
usage examples, notes etc
'''
# main code here
```

then pass it to the parser

```python
p = ArgumentParser(_help=__doc__)
```


### Auto-detect application name

This feature allows you to use script's real name in a help message, instead of
hardcoding it. It's enabled by default. To override it, pass `app_name`
parameter to the parser.

```python
p = ArgumentParser(_help=__doc__, app_name='foobar')
```

## ANSI colors

ANSI colors based on `blessing.Terminal` wrapper  and `log-color` option.  If
`auto` is selected, module will enable colors if output is terminal and disable
otherwise (redirection to pipe or file).

```python
from pydevkit.log import term_get

def main():
    term = term_get()
    log.warning("try %sred%s string", term.red, term.normal)
```


## Shell commands
TBD

## Misc
TBD
