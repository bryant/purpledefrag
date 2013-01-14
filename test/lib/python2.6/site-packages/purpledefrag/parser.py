from argparse import ArgumentParser, _HelpAction, SUPPRESS
from shlex import shlex
from purpledefrag.exceptions import PurpleArgError


class _PurpleHelpAction(_HelpAction):
	def __call__(self, parser, namespace, values, option_string = None):
		parser.error("")

class PurpleArgParser(ArgumentParser):
	def __init__(self, *args, **kwargs):
		oldhelp = kwargs.get("add_help", False)
		kwargs["add_help"] = False
		ArgumentParser.__init__(self, *args, **kwargs)

		self.register("action", "help", _PurpleHelpAction)
		if oldhelp:
			self.add_argument("-h", "--help", action = "help",
				default = SUPPRESS, help = "show this help message and exit")

	def parse_args(self, args):
		tokens = shlex(args, posix = True)
		tokens.whitespace_split = True

		try:
			z = tuple(tokens)
		except ValueError, e:
			raise PurpleArgError("^1" + e.message)
			#self.error(e.message)

		print "PurpleArgParser args: %s" % (z,)
		return ArgumentParser.parse_args(self, z)

	def exit(self, *args, **kwargs):
		raise NotImplementedError

	def error(self, message):
		if len(message) > 0:
			message = "^1" + message + "\n\n"

		message += "^3" + self.format_help()

		raise PurpleArgError(message)
