import logging

log = logging.getLogger(__name__)


conf = {
    "term": None,
}


def conf_set(key, value):
    conf[key] = value


def conf_get(key, value=None):
    return conf.get(key, value)
