import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import threading
import unittest
from io import open

os.chdir(os.path.dirname(os.path.realpath(__file__)))
supports_threading_excepthook = 'excepthook' in threading.__all__


def read_text_file(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as file:
        return file.read()


def write_text_file(filename, content, encoding='utf-8'):
    with open(filename, 'w', encoding=encoding) as file:
        file.write(content)


class TestTbtrim(unittest.TestCase):
    code_set_trim_rule = "tbtrim.set_trim_rule(lambda filename: os.path.basename(filename) == 'inner.py'{extra})"
    code_clear_trim_rule = "tbtrim.clear_trim_rule()"
    code_normal_main = textwrap.dedent("""\
        if __name__ == '__main__':
            main({extra})
    """)
    code_threading_main = textwrap.dedent("""\
        if __name__ == '__main__':
            import threading
            t = threading.Thread(target=main{extra})
            t.start()
            t.join()
    """)

    @classmethod
    def setUpClass(cls):
        cls.tmpd = tempfile.mkdtemp(prefix='tbtrim-test-')
        cls.template = read_text_file('template.py')
        shutil.copy('inner.py', cls.tmpd)
        shutil.copy(os.path.join('..', 'tbtrim.py'), cls.tmpd)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmpd, ignore_errors=True)

    def setUp(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra='')
        self.main_calls = self.code_normal_main.format(extra='')
        self.expect_trimmed = True

    def run_and_check_stderr(self, skip_check=False):
        filepath = os.path.join(self.tmpd, 'test.py')
        write_text_file(filepath, self.template.format(tbtrim_calls=self.tbtrim_calls, main_calls=self.main_calls))
        p = subprocess.Popen([sys.executable, filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.stderr = p.communicate()[1].decode()
        if skip_check:
            return
        if self.expect_trimmed:
            self.assertIn('inner.foo(exc)', self.stderr)
            self.assertNotIn('bar', self.stderr)
        else:
            self.assertIn('inner.foo(exc)', self.stderr)
            self.assertIn('bar(exc)', self.stderr)
            self.assertIn('baz(exc)', self.stderr)

    def test_predicate(self):
        self.run_and_check_stderr()

    def test_target_one(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', target=LookupError')
        self.main_calls = self.code_normal_main.format(extra='exc=LookupError')
        self.run_and_check_stderr()

    def test_target_multi(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', target=(LookupError, ValueError)')
        self.main_calls = self.code_normal_main.format(extra='exc=LookupError')
        self.run_and_check_stderr()

    def test_exclude_one(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', exclude=LookupError')
        self.main_calls = self.code_normal_main.format(extra='exc=LookupError')
        self.expect_trimmed = False
        self.run_and_check_stderr()

    def test_exclude_multi(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', exclude=(LookupError, ValueError)')
        self.main_calls = self.code_normal_main.format(extra='exc=LookupError')
        self.expect_trimmed = False
        self.run_and_check_stderr()

    def test_target_and_exclude_1(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', target=(LookupError, ValueError), exclude=(LookupError, NameError)')
        self.main_calls = self.code_normal_main.format(extra='exc=LookupError')
        self.expect_trimmed = False
        self.run_and_check_stderr()

    def test_target_and_exclude_2(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', target=(LookupError, ValueError), exclude=(ValueError, NameError)')
        self.main_calls = self.code_normal_main.format(extra='exc=LookupError')
        self.run_and_check_stderr()

    def test_not_strict(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', target=(LookupError, ValueError)')
        self.main_calls = self.code_normal_main.format(extra='exc=KeyError')
        self.run_and_check_stderr()

    def test_strict(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', target=(LookupError, ValueError), strict=True')
        self.main_calls = self.code_normal_main.format(extra='exc=KeyError')
        self.expect_trimmed = False
        self.run_and_check_stderr()

    def test_not_strict_exclude(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', target=(KeyError, ValueError), exclude=LookupError')
        self.main_calls = self.code_normal_main.format(extra='exc=KeyError')
        self.expect_trimmed = False
        self.run_and_check_stderr()

    def test_strict_exclude(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', target=(KeyError, ValueError), exclude=LookupError, strict=True')
        self.main_calls = self.code_normal_main.format(extra='exc=KeyError')
        self.run_and_check_stderr()

    def test_legacy_exception(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', exception=LookupError')
        self.main_calls = self.code_normal_main.format(extra='exc=LookupError')
        self.expect_trimmed = False
        self.run_and_check_stderr()

    def test_legacy_exception_conflict_with_exclude(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', exception=LookupError, exclude=ValueError')
        self.main_calls = self.code_normal_main.format(extra='exc=LookupError')
        self.run_and_check_stderr(skip_check=True)
        self.assertIn('''raise TypeError("cannot pass 'exclude' and 'exception' arguments at the same time")''', self.stderr)

    def test_clear(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra='') + '\n' + self.code_clear_trim_rule
        self.expect_trimmed = False
        self.run_and_check_stderr()

    @unittest.skipIf(not supports_threading_excepthook, 'threading.excepthook not supported')
    def test_threading(self):
        self.main_calls = self.code_threading_main.format(extra='')
        self.run_and_check_stderr()

    @unittest.skipIf(not supports_threading_excepthook, 'threading.excepthook not supported')
    def test_threading_with_parmeters_1(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', target=(KeyError, ValueError), exclude=(LookupError, NameError)')
        self.main_calls = self.code_threading_main.format(extra=', kwargs={"exc": KeyError}')
        self.expect_trimmed = False
        self.run_and_check_stderr()

    @unittest.skipIf(not supports_threading_excepthook, 'threading.excepthook not supported')
    def test_threading_with_parmeters_2(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', target=(KeyError, ValueError), exclude=(LookupError, NameError), strict=True')
        self.main_calls = self.code_threading_main.format(extra=', kwargs={"exc": KeyError}')
        self.run_and_check_stderr()

    @unittest.skipIf(not supports_threading_excepthook, 'threading.excepthook not supported')
    def test_threading_with_parmeters_3(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra=', target=(LookupError, ValueError), exclude=(ValueError, NameError)')
        self.main_calls = self.code_threading_main.format(extra=', kwargs={"exc": LookupError}')
        self.run_and_check_stderr()

    @unittest.skipIf(not supports_threading_excepthook, 'threading.excepthook not supported')
    def test_threading_clear(self):
        self.tbtrim_calls = self.code_set_trim_rule.format(extra='') + '\n' + self.code_clear_trim_rule
        self.main_calls = self.code_threading_main.format(extra='')
        self.expect_trimmed = False
        self.run_and_check_stderr()


if __name__ == '__main__':
    unittest.main()
