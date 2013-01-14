import re

class BaseRequest(object):
    _rawex = re.compile(
        "^(?P<clientnum>[0-9\-]+) "
        "(?P<ip>[0-9\.]+):(?P<qport>[0-9]+) "
        "\"(?P<name>[^\"]*)\" "
        "(?P<command>[^ ]+)"
        "(?P<rawargs>.*)$"
    )

    def __init__(self, raw):
        m = self._rawex.match(raw)
        assert m is not None, "Invalid request"

        d = m.groupdict()
        self.clientnum = int(d["clientnum"])
        self.ip = d["ip"]
        self.client = d["ip"] + "/" + d["qport"]
        self.name = d["name"]
        self.command = d["command"]
        self.rawargs = d["rawargs"].strip()
        self.args = self.rawargs.split()

