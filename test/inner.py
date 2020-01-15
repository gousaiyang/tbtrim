def foo(exc=None):
    bar(exc)


def bar(exc=None):
    baz(exc)


def baz(exc=None):
    raise exc or RuntimeError
