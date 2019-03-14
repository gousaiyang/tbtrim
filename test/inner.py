def foo():
    bar()


def bar():
    baz()


def baz():
    raise RuntimeError
