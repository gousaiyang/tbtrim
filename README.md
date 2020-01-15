# tbtrim

[![PyPI - Downloads](https://pepy.tech/badge/tbtrim)](https://pepy.tech/count/tbtrim)
[![PyPI - Version](https://img.shields.io/pypi/v/tbtrim.svg)](https://pypi.org/project/tbtrim)
[![PyPI - Format](https://img.shields.io/pypi/format/tbtrim.svg)](https://pypi.org/project/tbtrim)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tbtrim.svg)](https://pypi.org/project/tbtrim)
[![PyPI - Status](https://img.shields.io/pypi/status/tbtrim.svg)](https://pypi.org/project/tbtrim)
[![Travis CI - Status](https://img.shields.io/travis/gousaiyang/tbtrim.svg)](https://travis-ci.org/gousaiyang/tbtrim)
![License](https://img.shields.io/github/license/gousaiyang/tbtrim.svg)

`tbtrim` is a utility to trim Python traceback information. By assigning user-refined [`sys.excepthook`](https://docs.python.org/3/library/sys.html#sys.excepthook), one can easily customize the behavior after an exception is raise and uncaught, and just before the interpreter prints out the given traceback and exception to `sys.stderr`.

In a more human-readable way, `tbtrim` is to let you handle the last words of a program when it exits because of an exception.

## Installation

Simply run the following to install the current version from PyPI:

```shell
$ pip install tbtrim
```

Or install the latest version from the git repository:

```shell
git clone https://github.com/gousaiyang/tbtrim.git
cd tbtrim
pip install -e .
# and to update at any time
git pull
```

## Usage

> **set_trim_rule**(*predicate*, *target*=BaseException, *exclude*=None, *strict*=False)

Set the rule for trimming traceback (will set `sys.excepthook` and `threading.excepthook` if available).

You can determine whether to start to trim traceback items based on the filename.

**Args:**

- **predicate** (*function*): a function which takes one `str` parameter (the filename of a traceback item) and returns `bool` (returning `True` indicates that this traceback item and the following items should be trimmed)
- **target** (*class_or_tuple*): a tuple may be given as an exception to check against if to apply the rule for trimming its traceback
- **exclude** (*class_or_tuple*): a tuple may be given as an exception to check against if to **NOT** apply the rule for trimming its traceback
- **strict** (*bool*): indicate whether checking an exception against `target` and `exception` in a strict mode (setting `True` uses `is` to check; `False` uses `issubclass` to check)

> **clear_trim_rule**()

Clear the rule for trimming traceback (restore the excepthook).
