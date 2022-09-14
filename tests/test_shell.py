import unittest
from pydevkit.shell import Shell
from pydevkit.log import prettify


class ShellTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_input(self):
        sh = Shell()
        sh['dir'] = '/tmp'
        rc = sh("ls -1 %(dir)s", output=True)
        self.assertNotEqual(rc, '')
        rc = sh("ls -1 %(dir)s >/dev/null")
        self.assertEqual(rc, 0)
        sh['path'] = '/bin/bash'
        rc = sh("ls -1 %(path)s", output=True)
        self.assertIn('bash', rc)
        rc = sh.inp("ls -1 %(path)s")
        self.assertIn('bash', rc)

    def test_error_handling(self):
        sh = Shell()
        with self.assertRaises(Exception) as context:
            sh('ls -al /ffff 2>/dev/null')
        with self.assertRaises(Exception) as context:
            sh.inp('ls -al /ffff 2>/dev/null')

    def test_params(self):
        sh = Shell()
        pass
