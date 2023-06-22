import unittest
from pydevkit.shell import Shell


class ShellTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_input(self):
        sh = Shell()
        sh["dir"] = "/tmp"
        rc = sh("ls -1 %(dir)s", output=True)
        self.assertNotEqual(rc, "")
        rc = sh("ls -1 %(dir)s >/dev/null")
        self.assertEqual(rc, 0)
        sh["path"] = "/bin/bash"
        rc = sh("ls -1 %(path)s", output=True)
        self.assertIn("bash", rc)
        rc = sh.inp("ls -1 %(path)s")
        self.assertIn("bash", rc)

    def test_error_handling(self):
        sh = Shell()
        with self.assertRaises(Exception):
            sh("ls -al /ffff 2>/dev/null")
        with self.assertRaises(Exception):
            sh.inp("ls -al /ffff 2>/dev/null")

    def test_params(self):
        sh = Shell()
        sh["a1"] = "val-a1"
        sh["a2"] = "val-a2"
        rc = sh.inp("echo %(a1)s %(a2)s")
        answer = "val-a1 val-a2"
        self.assertEqual(rc, answer)
