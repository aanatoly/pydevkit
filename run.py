#!/usr/bin/env python3
'''
Main description

EPILOG:
Example1

Example2
'''


import sys
sys.dont_write_bytecode = True


import pydevkit.log.config  # noqa: F401
from pydevkit.log import conf_get, term_get, prettify
from pydevkit.argparse import ArgumentParser
from pydevkit.shell import Shell
import threading

import logging
log = logging.getLogger(__name__)


def get_args():
    p = ArgumentParser(_help=__doc__, version='1.2.3')
    # FIXME: add your args here

    return p.args_resolve()


def main():
    Args, UnknownArgs = get_args()
    if UnknownArgs:
        log.warning("Unknown arguments: %s", UnknownArgs)
        # exit(1)
    threading.current_thread().name = 'main'
    kwargs = {'extra': {'ip': '10.0.0.1'}}
    for a in ['debug', 'info', 'warning', 'error', 'critical']:
        fn = getattr(log, a)
        fn("%s msg", a)
        fn("%s msg", a, extra=kwargs)
    term = term_get()
    print("try %sred%s string" % (term.red, term.normal))
    print("log level %s" % conf_get('level'))

    sh = Shell()
    sh('echo test shell class')


if __name__ == '__main__':
    main()
