import unittest
from pydevkit.shell import Shell
from pydevkit.log import prettify


class PrettifyTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_formatting(self):
        rc = {
            'list': [1,2,3],
            'dict': {
                'func': self.setUp,
                'list': [1,2,3]
            },
            'obj': self
        }
        answer = '''{
    "dict": {
        "func": "<bound method PrettifyTest.setUp of <tests.test_log.PrettifyTest testMethod=test_formatting>>",
        "list": [
            1,
            2,
            3
        ]
    },
    "list": [
        1,
        2,
        3
    ],
    "obj": "test_formatting (tests.test_log.PrettifyTest)"
}'''
        rc = prettify(rc)
        self.assertEqual(rc, answer)
