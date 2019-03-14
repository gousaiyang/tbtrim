import os
import subprocess
import sys
import unittest

os.chdir(os.path.dirname(os.path.realpath(__file__)))


class TestTbtrim(unittest.TestCase):
    def test_predicate(self):
        p = subprocess.Popen([sys.executable, 'test_predicate.py'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stderr = p.communicate()[1].decode()
        self.assertNotIn('bar()', stderr)
        self.assertIn('inner.foo()', stderr)


if __name__ == '__main__':
    unittest.main()
