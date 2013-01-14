from re import compile
from textwrap import TextWrapper


def iterchunk(iterable, n):
	"""Returns the iterable in n-sized chunks."""
	for i in range(0, len(iterable), n):
		yield iterable[i:i + n]

class BaseRequest(object):
	_rawex = compile(
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

class BaseResponse(object):
	def __init__(self, response, clientnum = None):
		self.response = response + "\n"
		self.clientnum = clientnum

	def __call__(self, request, server):
		clientnum = self.clientnum or request.clientnum
		self.emit(clientnum, server)

	def emit(self, clientnum, server):
		raise NotImplementedError

class ConsoleResponse(BaseResponse):
	consolewrap = TextWrapper(
		width = 768,
		expand_tabs = True,
		replace_whitespace = False,
		drop_whitespace = False
	)

	def emit(self, clientnum, server):
		for chunk in self.consolewrap.wrap(self.response):
			server.clientprint(clientnum, chunk)

class RawChatResponse(BaseResponse):
	chatwrapper = TextWrapper(
		width = 150,
		expand_tabs = True,
		replace_whitespace = False
	)

	def emit(self, clientnum, server):
		for chunk in self.chatwrapper.wrap(self.response):
			server.clientsay(clientnum, chunk)

class HUDResponse(BaseResponse):
	def emit(self, clientnum, server):
		server.clienthudprint(clientnum, self.response)

class ChatResponse(RawChatResponse):
	def __init__(self, name, response, clientnum = None):
		if len(name) > 150:
			raise Exception("NamedChatResponse.name is too long: " + name)

		RawChatResponse.__init__(self, response, clientnum)

		self.name = name
		self.wrapper = TextWrapper(
			width = 150 - len(name),
			expand_tabs = True,
			replace_whitespace = False
		)

	def emit(self, clientnum, server):
		for chunk in self.wrapper.wrap(self.response):
			server.clientsay(clientnum,
				self.name + "^7: ^2" + chunk)

class BunnyResponse(ChatResponse):
	name = "defra^5g ^2b^7unny"
	def __init__(self, response, clientnum = None):
		ChatResponse.__init__(self, self.name, response, clientnum)


if __name__ == "__main__":
	from optparse import OptionParser

	teststrings = [
		"0 1.2.3.4:5678 \"lala\" login",
		"0 1.2.3.4:5678 \"lala\" login 123 2 -d"
	]

	for test in teststrings:
		print "[%s]: [%s]" % (test, BaseRequest(test).args)
		print OptionParser().parse_args(args = [test])
