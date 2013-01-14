from purpledefrag import (BaseRequest, PurpleConnection,
	MessageSocket, ConsoleResponse)
from purpledefrag.exceptions import PurpleArgError, InvalidCommandError


class PurpleApp(object):
	def __init__(self, host, rconPassword, routes):
		self.messages = MessageSocket("localhost")
		self.server = PurpleConnection(host, rconPassword)
		self.routes = routes

	def notify(self):
		msgs = self.messages
		server = self.server
		recognized = " " + " ".join(self.routes.getRecognized()) + " "

		server.rcon("ext_notify \"%s:%d\"" % (msgs.host, msgs.port))
		server.rcon("ext_cmds \"%s\"" % recognized)

	def serveForever(self):
		while True:
			raw = self.messages.listen()
			print "Raw:", raw.strip()

			try:
				request = BaseRequest(raw)
			except AssertionError:
				print "Error formatting request"
				continue

			try:
				Controller, args = self.routes.match(request)
			except PurpleArgError, e:
				response = ConsoleResponse(e.message)
			except InvalidCommandError:
				print "Invalid command"
				continue
			else:
				response = Controller(request, args)()

			if response:
				print "Replying:", response.response[:32]
				response(request, self.server)
