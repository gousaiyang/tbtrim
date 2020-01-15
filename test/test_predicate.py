import os
import sys

ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, '..')))
import tbtrim
sys.path.pop(0)

import inner

tbtrim.set_trim_rule(lambda filename: os.path.split(filename)[-1] == 'inner.py')


def main():
    inner.foo()


if __name__ == '__main__':
    main()
