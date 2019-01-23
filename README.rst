======
tbtrim
======

``tbtrim`` is a utility to trim Python traceback information.
By assigning user-refined |sys_excepthook|_, one can easily
customise the behaviour after an exception is raise and uncaught,
and just before the interpreter prints out the given traceback
and exception to ``sys.stderr``.

In a more human-readable way, ``tbtrim`` is to let you handle
the last words of a program when it exits because of an exception.

.. |sys_excepthook| replace:: ``sys.excepthook``
.. _sys_excepthook: https://docs.python.org/library/sys.html#sys.excepthook

Installation
------------

Simply run the following to install the current version from PyPI:

.. code:: shell

  $ pip install tbtrim

Or install the latest version from the git repository:

.. code:: shell

  git clone https://github.com/gousaiyang/tbtrim.git
  cd tbtrim
  pip install -e .
  # and to update at any time
  git pull

Usage
-----

- ``set_trim_rule(predicate)``

  Set the rule for trimming traceback (will set ``sys.excepthook``).

  You can determine whether to start to trim traceback items based
  on the filename.

  Args:
    ``predicate`` (function)
      a function which takes one ``str`` parameter (the filename of
      a traceback item) and returns ``bool`` (returning ``True``
      indicates that this traceback item and the following items
      should be trimmed)

- ``clear_trim_rule()``

  Clear the rule for trimming traceback (restore the excepthook).
