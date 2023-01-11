import unittest
from pydevkit.argparse import EnvAction
from argparse import ArgumentParser as LibArgumentParser
from pydevkit.argparse import PdkArgumentParser
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
        libp.add_argument(
            "--level",
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

    def tearDown(self):
        pass

    def do_test(self, envval, show_default, show_envvar, answer):
        if envval:
            os.environ['PDK_LEVEL'] = envval

        def _fmt(prog):
            return PdkHelpFormatter(prog, show_envvar=show_envvar,
                                    show_default=show_default)

        kwargs = {'formatter_class': _fmt}
        libp = LibArgumentParser(**kwargs)
        libp.add_argument(
            "--level",
            help="n/a",
            metavar="arg",
            action=EnvAction,
            envvar='PDK_LEVEL',
            default="val-default")
        rc = libp.format_help()
        rc = [line for line in rc.splitlines() if line.startswith('  --level')]
        rc = rc[0]
        # print("rc", rc)
        self.assertEqual(rc, answer)

    def test_env_no_show_def_yes_show_env_yes(self):
        answer = "  --level arg  n/a (default: val-default) (envvar: PDK_LEVEL)"
        self.do_test(None, True, True, answer)

    def test_env_yes_show_def_yes_show_env_yes(self):
        answer = "  --level arg  n/a (default: val-default) (envvar: PDK_LEVEL)"
        self.do_test('val-env', True, True, answer)

    def test_env_yes_show_def_no_show_env_yes(self):
        answer = "  --level arg  n/a (envvar: PDK_LEVEL)"
        self.do_test('val-env', False, True, answer)

    def test_env_yes_show_def_yes_show_env_no(self):
        answer = "  --level arg  n/a (default: val-default)"
        self.do_test('val-env', True, False, answer)

    def test_env_yes_show_def_no_show_env_no(self):
        answer = "  --level arg  n/a"
        self.do_test('val-env', False, False, answer)


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


class PdkArgumentParserTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def do_help_test(self, **kwargs):
        p = PdkArgumentParser(**kwargs)
        rc = p.format_help()
        # print("help", rc)
        return rc

    def test_version(self):
        answer = '  --version '
        rc = self.do_help_test(version='1.2.3')
        self.assertIn(answer, rc)
        rc = self.do_help_test()
        self.assertNotIn(answer, rc)

    def test_usage(self):
        answer = ' [--log-'
        rc = self.do_help_test(usage="full")
        self.assertIn(answer, rc)
        rc = self.do_help_test(usage="short")
        self.assertNotIn(answer, rc)
        answer = '[logging]'
        self.assertIn(answer, rc)

    def test_help(self):
        help = '''
Some help 1
another line

EPILOG:
epilog1
epilog2
'''
        rc = self.do_help_test(help=help)
        answer = help.split('\nEPILOG:\n')
        self.assertIn(answer[0], rc)
        self.assertIn(answer[1], rc)
