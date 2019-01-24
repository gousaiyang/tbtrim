import sys
import traceback

old_excepthook = sys.excepthook


def _exception_predicate(etype, target, exception, strict):
    '''Determine whether to trim traceback of certain exception.'''
    if not isinstance(target, tuple):
        target = (target,)
    if not isinstance(exception, tuple):
        exception = (exception,)

    if strict:
        target_flag = any(map(lambda e: etype is e, target))
        except_flag = all(map(lambda e: etype is not e, exception))
    else:
        target_flag = any(map(lambda e: issubclass(etype, e), target))
        except_flag = any(map(lambda e: not issubclass(etype, e), exception))

    return (target_flag and except_flag)


def set_trim_rule(predicate, target=BaseException, exception=(),
                  strict=False):
    '''
    Set the rule for trimming traceback (will set `sys.excepthook`).

    You can determine whether to start to trim traceback items based on the
    filename.

    Args:
        predicate (function): a function which takes one `str` parameter
            (the filename of a traceback item) and returns `bool` (returning
            `True` indicates that this traceback item and the following items
            should be trimmed)

        target (class_or_tuple): a tuple may be given as an exception to check
            against if to apply the rule for trimming its traceback

        exception (class_or_tuple): a tuple may be given as an exception to
            check against if NOT to apply the rule for trimming its traceback

        strict (bool): indicate whether checking an exception against `target`
            and `exception` in a strict mode (setting `True` uses `is` to check;
            `False` uses `issubclass` to check)
    '''
    def tbtrim_excepthook(etype, value, tb):
        if _exception_predicate(etype, target, exception, strict):
            ptb = tb
            limit = 0

            while ptb:
                if predicate(ptb.tb_frame.f_code.co_filename):
                    break

                limit += 1
                ptb = ptb.tb_next
        else:
            limit = None

        traceback.print_exception(etype, value, tb, limit)

    sys.excepthook = tbtrim_excepthook


def clear_trim_rule():
    '''Clear the rule for trimming traceback (restore the excepthook).'''
    sys.excepthook = old_excepthook


__all__ = ['set_trim_rule', 'clear_trim_rule']
