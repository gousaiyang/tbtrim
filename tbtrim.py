import sys
import threading
import traceback

supports_threading_excepthook = 'excepthook' in threading.__all__

old_sys_excepthook = sys.excepthook

if supports_threading_excepthook:  # novermin
    old_threading_excepthook = threading.excepthook


def _exception_predicate(etype, target, exclude, strict):
    """Determine whether to trim traceback of certain exception."""
    if not isinstance(target, tuple):
        target = (target,)
    if not isinstance(exclude, tuple):
        exclude = (exclude,)

    if strict:
        target_flag = any(map(lambda e: etype is e, target))
        except_flag = all(map(lambda e: etype is not e, exclude))
    else:
        target_flag = any(map(lambda e: issubclass(etype, e), target))
        except_flag = all(map(lambda e: not issubclass(etype, e), exclude))

    return target_flag and except_flag


def set_trim_rule(predicate, target=BaseException, exclude=None, strict=False,
                  exception=None):
    """Set the rule for trimming traceback (will set `sys.excepthook` and
    `threading.excepthook` if available).

    You can determine whether to start trimming traceback items based on the filename
    (using `predicate`), and can choose to trim traceback only for some certain
    exceptions (using `target` and `exclude`).

    Args:
        predicate (function): a function which takes one `str` parameter
            (the filename of a traceback item) and returns `bool` (returning
            `True` indicates that this traceback item and the following items
            should be trimmed)

        target (class_or_tuple): an exception or a tuple of exceptions may be given to
            trim traceback only for those exceptions

        exclude (class_or_tuple): an exception or a tuple of exceptions may be given to
            exclude them from traceback trimming

        strict (bool): indicate whether to check an exception against `target` and
            `exclude` in a strict mode (setting `True` uses `is` to check, `False` uses
            `issubclass` to check)

        exception (class_or_tuple): this is a deprecated alias of `exclude`, retained for
            backward compatibility

    """
    if exclude is not None and exception is not None:
        raise TypeError("cannot pass 'exclude' and 'exception' arguments at the same time")
    if exclude is None:
        exclude = exception
        if exclude is None:
            exclude = ()

    def tbtrim_excepthook(etype, value, tb):
        if _exception_predicate(etype, target, exclude, strict):
            ptb = tb
            limit = 0
            while ptb:
                if predicate(ptb.tb_frame.f_code.co_filename):
                    break
                limit += 1
                ptb = ptb.tb_next
        else:
            limit = None

        if limit == 0:
            traceback.print_exception(etype, value, None)
        else:
            traceback.print_exception(etype, value, tb, limit)

    sys.excepthook = tbtrim_excepthook
    if supports_threading_excepthook:  # novermin
        threading.excepthook = lambda args: tbtrim_excepthook(args.exc_type,
                                                              args.exc_value,
                                                              args.exc_traceback)


def clear_trim_rule():
    """Clear the rule for trimming traceback (restore the excepthooks)."""
    sys.excepthook = old_sys_excepthook
    if supports_threading_excepthook:  # novermin
        threading.excepthook = old_threading_excepthook


__all__ = ['set_trim_rule', 'clear_trim_rule']
