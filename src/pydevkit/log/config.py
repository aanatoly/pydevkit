import logging.config
import os
import json
import sys

from . import term_set
from pydevkit.conf import conf_set, conf_get
from pydevkit.argparse import LoggingArgumentParser


defaultConf = {
    "version": 1,
    "disable_existing_loggers": True,
    "loggers": {
        "": {"level": "%LEVEL%", "handlers": ["app_handler"]},
        "trace": {"level": "WARNING"},
        "lu": {"level": "INFO"},
        "urllib3": {"level": "INFO"},
        "requests": {"level": "WARNING"},
    },
    "handlers": {
        "null_handler": {"class": "logging.NullHandler"},
        "app_handler": {
            "level": "DEBUG",
            "formatter": "%FMT%",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "filters": ["app_name", "time", "extra"],
        },
    },
    "filters": {
        "app_name": {"()": "pydevkit.log.AppNameFilter", "threads": "no"},
        "time": {
            "()": "pydevkit.log.TimeFilter",
            "format": "%DATE%",
        },
        "extra": {"()": "pydevkit.log.ExtraFilter"},
    },
    "formatters": {
        "app_mini": {
            "()": "pydevkit.log.ColorLevelFormatter",
            "format": "%(clr_details)s%(time)s%(clr_reset)s :: %(appname)s :: "
            "%(clr_level)s%(levelname)-5s%(clr_reset)s :: "
            "%(message)s %(extra)s",
        },
        "app": {
            "()": "pydevkit.log.ColorLevelFormatter",
            "format": "%(clr_details)s%(time)s%(clr_reset)s :: %(appname)s :: "
            "%(clr_level)s%(levelname)-5s%(clr_reset)s :: "
            "%(message)s "
            "%(extra)s :: %(clr_details)s%(name)s%(clr_reset)s",
        },
        "json_mini": {
            "()": "pydevkit.log.JsonFormatter",
            "format": "%(appname)s %(name)s %(levelname)s %(message)s "
            "%(extra)s",
        },
        "json": {
            "()": "pydevkit.log.JsonFormatter",
            "format": "%(time)s %(appname)s %(levelno)s %(levelname)s "
            "%(message)s %(extra)s %(name)s",
        },
    },
}


def _get_conf(kwargs):
    ovals = {
        "level": "INFO",
        "handler": "app_mini",
        "date": "datetime",
        "color": "auto",
        "threads": "yes",
    }
    vals = dict(ovals)
    vals.update(kwargs)
    conf_set("level", vals["level"].upper())
    defaultConf["loggers"][""]["level"] = conf_get("level")
    defaultConf["handlers"]["app_handler"]["formatter"] = vals["handler"]
    if vals["handler"] == "app_mini":
        if "date" not in kwargs:
            vals["date"] = "time"
    color = vals["color"]
    if color == "auto":
        color = "yes" if sys.stderr.isatty() else "no"
    conf_set("color", color)
    term_set(color)

    defaultConf["filters"]["time"]["format"] = vals["date"]
    defaultConf["filters"]["app_name"]["threads"] = vals["threads"]
    return defaultConf


def _logging_config():
    # print("X"* 20, "config log")
    conf_path = os.environ.get("PYDEVKIT_LOG_CONFIG", None)
    if conf_path:
        if conf_path.endswith(".json"):
            conf = json.load(open(conf_path, "r"))
            logging.config.dictConfig(conf)
        else:
            logging.config.fileConfig(conf_path)
    else:
        p = LoggingArgumentParser()
        Args, UnknownArgs = p.parse_known_args()
        args = vars(Args)
        kwargs = {}
        for k, v in args.items():
            # print("Args", k, v)
            if not k.startswith("log_"):
                continue
            kwargs[k[4:]] = v

        conf = _get_conf(kwargs)
        logging.config.dictConfig(conf)
    log = logging.getLogger(__name__)
    log.debug("logging: configured")


_logging_config()

# }}}
