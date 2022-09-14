import unittest
from pydevkit.argparse import EnvAction
from argparse import ArgumentParser as LibArgumentParser
from pydevkit.argparse import ArgumentParser
from pydevkit.argparse import LoggingArgumentParser
from pydevkit.argparse import PdkHelpFormatter
from pydevkit.log import prettify
import os


class EnvActionTest(unittest.TestCase):
    def setUp(self):
        if 'PDK_LEVEL' in os.environ:
            del os.environ['PDK_LEVEL']

    def tearDown(self):
        pass

    def libp_new(self, **kwargs):
        libp = LibArgumentParser(**kwargs)
        libp.add_argument("--level",
                       help="n/a",
                       metavar="arg",
                       action=EnvAction,
                       envvar='PDK_LEVEL',
                       default="val-default")
        return libp


    def test_cmd_yes_env_no(self):
        answer = '''{
    "level": "val-cmd"
}'''
        libp = self.libp_new()
        cmd = '--level val-cmd'.split()
        args, uargs = libp.parse_known_args(cmd)
        args = prettify(vars(args))
        self.assertEqual(args, answer)

    def test_cmd_yes_env_yes(self):
        os.environ['PDK_LEVEL'] = 'val-env'
        self.test_cmd_yes_env_no()


    def test_cmd_no_env_yes(self):
        cmd = []
        os.environ['PDK_LEVEL'] = 'val-env'
        libp = self.libp_new()
        args, uargs = libp.parse_known_args(cmd)
        args = prettify(vars(args))
        answer = '''{
    "level": "val-env"
}'''
        self.assertEqual(args, answer)

    def test_cmd_no_env_no(self):
        cmd = []
        libp = self.libp_new()
        args, uargs = libp.parse_known_args(cmd)
        args = prettify(vars(args))
        answer = '''{
    "level": "val-default"
}'''
        self.assertEqual(args, answer)


class PdkHelpFormatterTest(unittest.TestCase):
    def setUp(self):
        if 'PDK_LEVEL' in os.environ:
            del os.environ['PDK_LEVEL']
        self.answer = "  --level arg  n/a (default: val-default) (envvar: PDK_LEVEL)"

    def tearDown(self):
        pass

    def libp_new(self, **kwargs):
        kwargs['formatter_class'] = PdkHelpFormatter
        libp = LibArgumentParser(**kwargs)
        libp.add_argument("--level",
                       help="n/a",
                       metavar="arg",
                       action=EnvAction,
                       envvar='PDK_LEVEL',
                       default="val-default")
        return libp

    def test_env_no(self):
        libp = self.libp_new()
        rc = libp.format_help()
        rc = [line for line in rc.splitlines() if line.startswith('  --level')]
        rc = rc[0]
        self.assertEqual(rc, self.answer)

    def test_env_yes(self):
        os.environ['PDK_LEVEL'] = 'val-env'
        self.test_env_no()


class LoggingArgumentParserTest(unittest.TestCase):
    def setUp(self):
        if 'PYDEVKIT_LOG_LEVEL' in os.environ:
            del os.environ['PYDEVKIT_LOG_LEVEL']

    def tearDown(self):
        pass

    def libp_new(self, **kwargs):
        libp = LoggingArgumentParser(**kwargs)
        return libp

    def dict_eq(self, a1, a2):
        a1 = prettify(vars(a1))
        a2 = prettify(vars(a2))
        return a1 == a2

    def parse_args(self, elevel, clevel, alevel):
        answer = {
            "log_color": "auto",
            "log_date": "datetime",
            "log_handler": "app_mini",
            "log_level": "info",
            "log_threads": "no"
        }
        if alevel:
            answer['log_level'] = alevel
        if elevel:
            os.environ['PYDEVKIT_LOG_LEVEL'] = elevel
        if clevel:
            cmd = ['--log-level', clevel]
        else:
            cmd = []
        libp = self.libp_new()
        args, uargs = libp.parse_known_args(cmd)
        args = vars(args)
        # print("args", args)
        self.assertEqual(args, answer)

    def test_cmd_no_env_no(self):
        self.parse_args(None, None, None)

    def test_cmd_no_env_yes(self):
        self.parse_args('error', None, 'error')

    def test_cmd_yes_env_yes(self):
        self.parse_args('error', 'debug', 'debug')
