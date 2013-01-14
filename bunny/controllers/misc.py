from purpledefrag.app.controllers.base import *
from purpledefrag import BunnyResponse
from time import strftime, localtime


class HelpController(BaseController):
	opt = PurpleArgParser(prog = "/wtf")

	def command(self):
		endpoints = ", ".join(
			("/" + t for t in g.routes.getRecognized())
		)

		return ConsoleResponse("^5Command synopsis:\n\t" + endpoints)

class TimeController(BaseController):
	opt = PurpleArgParser(prog = "/time")

	def command(self):
		return ConsoleResponse(
			strftime("^3%a %d %b %Y %H:%M:%S %Z",localtime())
		)

class MeController(BaseController):
	@classmethod
	def parseArgs(cls, raw):
		return None

	def command(self):
		request = self.request

		if len(request.rawargs) > 0:
			return RawChatResponse(
				" * %s^6 %s" % (request.name, request.rawargs),
				clientnum = -1
			)

class TomController(BaseController):
	opt = PurpleArgParser(prog = "/tom")

	def command(self):
		return BunnyResponse("^2Hippeh luf peace. Bunny luf hippeh.",
			clientnum = -1)

class ReminderController(BaseController):
	opt = PurpleArgParser(prog = "/reminder")

	def command(self):
		request = self.request
		cmd = request.command[1:]

		if request.command.startswith('!') and cmd.isalpha():
			if cmd in g.routes.getRecognized():
				return BunnyResponse("^7%s^2, try ^5/%s^2." %
					(request.name, request.command[1:]),
					clientnum = -1
				)
			else:
				return BunnyResponse("^2I forgot what to do with !%s. "
					"Use ^7/h^2 for a list of tricks I can do." % cmd,
					clientnum = -1)

def upvote(request):
	return ConsoleResponse("^6You lufs dis mup.")

def downvote(request):
	return ConsoleResponse("^6You ^1rage ^6dis mup!")
