import json
import re


class _AllEncoder(json.JSONEncoder):
    reg = re.compile("\\s+at\\s+[^>]+")

    def no_addr(self, s):
        return self.reg.sub("", s)

    def default(self, obj):
        if hasattr(obj, "__call__"):
            return self.no_addr(str(obj))
        elif isinstance(obj, object):
            return self.no_addr(str(obj))
        try:
            return json.JSONEncoder.default(self, obj)
        except Exception:
            return str(obj)


def prettify(eobj):
    return json.dumps(eobj, indent=4, sort_keys=True, cls=_AllEncoder)
