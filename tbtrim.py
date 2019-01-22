import sys
import traceback

old_excepthook = sys.excepthook


def set_trim_rule(predicate):
    '''
    Set the rule for trimming traceback (will set `sys.excepthook`).

    You can determine whether to start to trim traceback items based on the
    filename.

    Args:
        predicate (function): a function which takes one `str` parameter
            (the filename of a traceback item) and returns `bool` (returning
            `True` indicates that this traceback item and the following items
            should be trimmed)
    '''
    def tbtrim_excepthook(etype, value, tb):
        ptb = tb
        remaining_items = 0

        while ptb:
            if predicate(ptb.tb_frame.f_code.co_filename):
                break

            remaining_items += 1
            ptb = ptb.tb_next

        traceback.print_exception(etype, value, tb, remaining_items)

    sys.excepthook = tbtrim_excepthook


def clear_trim_rule():
    '''Clear the rule for trimming traceback (restore the excepthook).'''
    sys.excepthook = old_excepthook


__all__ = ['set_trim_rule', 'clear_trim_rule']
