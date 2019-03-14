import os
import sys
sys.path.append('..')

import tbtrim

import inner

tbtrim.set_trim_rule(lambda filename: os.path.split(filename)[-1] == 'inner.py')


def main():
    inner.foo()


if __name__ == '__main__':
    main()
