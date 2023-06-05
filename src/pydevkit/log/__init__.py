from pydevkit.term import Terminal
from pydevkit.conf import conf_set, conf_get
from .extra import prettify
from .base import ColorLevelFormatter, JsonFormatter
from .base import TimeFilter, ExtraFilter, LogNameFilter, AppNameFilter


# {{{
# FIXME: remove this, use term_get from term.py
def term_set(state):
    conf_set("term", Terminal(state))


def term_get():
    return conf_get("term")


# }}}


__all__ = [
    "prettify",
    "ColorLevelFormatter",
    "JsonFormatter",
    "TimeFilter",
    "ExtraFilter",
    "LogNameFilter",
    "AppNameFilter",
]
