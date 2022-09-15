#!/usr/bin/env python3
'''
Demonstrates pydevkit features.

EPILOG:
Example1:
PYDEVKIT_LOG_HANDLER=app ./script --log-level=debug

Example2:
./script --log-level=debug --log-handler=json
'''


import pydevkit.log.config  # noqa: F401
from pydevkit.conf import conf_set, conf_get
from pydevkit.log import prettify
from pydevkit.term import term_get
from pydevkit.argparse import ArgumentParser
from pydevkit.shell import Shell
import threading

import logging
log = logging.getLogger(__name__)


def get_args():
    p = ArgumentParser(help=__doc__, version='1.2.3', usage="full")
    # FIXME: add your args here
    p.add_argument("--file", help="file arg")

    return p.parse_known_args()


def main():
    Args, UnknownArgs = get_args()
    if UnknownArgs:
        log.warning("Unknown arguments: %s", UnknownArgs)
        # exit(1)
    threading.current_thread().name = 'main'

    print(">> Test logging")
    kwargs = {'extra': {'ip': '10.0.0.1'}}
    for a in ['debug', 'info', 'warning', 'error', 'critical']:
        fn = getattr(log, a)
        fn("%s msg", a)
        fn("%s msg", a, extra=kwargs)
    log.debug("kwargs\n%s", prettify(kwargs))

    print(">> Test terminal colors")
    term = term_get()
    print("try %sred%s string" % (term.red, term.normal))

    print(">> Test conf")
    print("conf: log level %s" % conf_get('level'))

    print(">> Test shell")
    sh = Shell()
    sh('echo hello, world')


if __name__ == '__main__':
    main()
