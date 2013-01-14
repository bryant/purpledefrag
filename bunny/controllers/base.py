from purpledefrag import ConsoleResponse, RawChatResponse, PurpleArgParser
import purpledefrag.app.g as g


class BaseController(object):
	def __init__(self, request, args):
		self.request = request
		self.args = args

	def __call__(self):
		return self.command()

	@classmethod
	def parseArgs(cls, raw):
		return cls.opt.parse_args(args = raw)

if __name__ == "__main__":
	from purpledefrag import BaseRequest

	teststrings = [
		"23 1.2.3.4:56 \"asdf\" logs",
		"2 4.5.6.7:23 \"dsd\" random --rockets"
	]
	b = BaseController()

	for test in teststrings:
		print test
		print b(BaseRequest(test))
