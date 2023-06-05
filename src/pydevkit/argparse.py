import argparse
import os
from pydevkit.log import prettify

import logging

# log = logging.getLogger(__name__)


class EnvAction(argparse.Action):
    def __init__(self, envvar, default=None, **kwargs):
        self.envvar = envvar
        self.orig_default = default
        if envvar in os.environ:
            default = os.environ[envvar]
        super(EnvAction, self).__init__(default=default, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


class PdkHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def __init__(self, prog, show_default=True, show_envvar=True, **kwargs):
        super().__init__(prog, **kwargs)
        self.show_default = show_default
        self.show_envvar = show_envvar

    def _get_help_string(self, action):
        help = action.help
        defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
        if (
            self.show_default
            and ("%(default)" not in action.help)
            and (action.default is not argparse.SUPPRESS)
            and (action.option_strings or action.nargs in defaulting_nargs)
        ):
            help += " (default: %(default)s)"
        if hasattr(action, "orig_default"):
            help = help.replace("%(default)", "%(orig_default)")

        if self.show_envvar and hasattr(action, "envvar"):
            help += " (envvar: %(envvar)s)"

        return help

    def _format_usage_short(self, usage, actions, groups, prefix):
        groups = []
        # print("XXX: add_usage: usage:", usage)
        for action in actions:
            tmp = getattr(action, "container", None)
            if tmp.title and tmp.title not in groups:
                groups.append(tmp.title)
        groups = " ".join(["[" + g + "]" for g in groups])
        return "usage: %s %s\n" % (self._prog, groups)

    def add_usage(self, usage, actions, groups, prefix=None):
        if usage == "short":
            args = usage, actions, groups, prefix
            self._add_item(self._format_usage_short, args)
        elif usage == "full" or usage is None:
            args = None, actions, groups, prefix
            self._add_item(self._format_usage, args)
        else:
            args = usage, actions, groups, prefix
            self._add_item(self._format_usage, args)


class LoggingArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(add_help=False)
        log_levels = ["debug", "info", "warning", "error", "critical"]
        log_handlers = ["app", "app_mini", "json", "json_mini"]
        # p = self.add_argument_group('logging', 'logging configuration')
        p = self.add_argument_group("logging", None)
        p.add_argument(
            "--log-level",
            help="values: %(choices)s",
            metavar="arg",
            choices=log_levels,
            action=EnvAction,
            envvar="PYDEVKIT_LOG_LEVEL",
            default="info",
        )
        p.add_argument(
            "--log-color",
            help="colorfull logs: %(choices)s",
            metavar="arg",
            choices=["auto", "yes", "no"],
            action=EnvAction,
            envvar="PYDEVKIT_LOG_COLOR",
            default="auto",
        )
        p.add_argument(
            "--log-handler",
            help="message format: %(choices)s",
            metavar="arg",
            choices=log_handlers,
            action=EnvAction,
            envvar="PYDEVKIT_LOG_HANDLER",
            default="app_mini",
        )
        p.add_argument(
            "--log-date",
            help="date format: 'datetime', 'date', 'time'"
            " or strftime format eg '%%Y-%%m-%%d'",
            metavar="arg",
            action=EnvAction,
            envvar="PYDEVKIT_LOG_DATE",
            default="datetime",
        )
        p.add_argument(
            "--log-threads",
            help="show thread name: %(choices)s",
            metavar="arg",
            choices=["yes", "no"],
            action=EnvAction,
            envvar="PYDEVKIT_LOG_THREADS",
            default="no",
        )


class PdkArgumentParser(argparse.ArgumentParser):
    def __init__(
        self,
        version=None,
        usage="full",
        show_default=True,
        show_envvar=True,
        **kwargs
    ):
        def _fmt(prog):
            return PdkHelpFormatter(
                prog, show_envvar=show_envvar, show_default=show_default
            )

        kwargs["formatter_class"] = _fmt

        app_help = kwargs.get("help")
        if app_help is not None:
            tmp = app_help.split("\nEPILOG:\n")
            kwargs["description"] = tmp[0]
            kwargs["epilog"] = tmp[1] if len(tmp) == 2 else None
            del kwargs["help"]

        kwargs["usage"] = usage

        app_parents = kwargs.get("parents", [])
        kwargs["parents"] = app_parents + [LoggingArgumentParser()]

        super().__init__(**kwargs)
        if version:
            self.add_argument("--version", action="version", version=version)

    def parse_known_args(self, args=None, namespace=None):
        Args, UnknownArgs = super().parse_known_args(args, namespace)
        if UnknownArgs:
            if UnknownArgs[0] == "--":
                del UnknownArgs[0]
        # print("X"* 20, "parse args", prettify(vars(Args)))
        log = logging.getLogger(__name__)
        log.debug(
            "argparse:\nArgs: %s\nUnknownArgs: %s\n",
            prettify(vars(Args)),
            UnknownArgs,
        )
        return Args, UnknownArgs


class ArgumentParser(PdkArgumentParser):
    def __init__(self, _help=None, help=None, **kwargs):
        kwargs["help"] = _help or help
        super().__init__(**kwargs)

    def args_resolve(self, args=None):
        return self.parse_known_args(args)
