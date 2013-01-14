from purpledefrag.exceptions import InvalidCommandError


class Map(object):
	def __init__(self):
		self.routes = {}
		self.sv_only = set()

	def addRule(self, name, endpoint):
		assert hasattr(endpoint, "__call__"), "Endpoint not callable"
		assert name not in self.routes, "Map '%s' already exists" % name

		if hasattr(endpoint, "_server_only") and endpoint._server_only:
			self.sv_only.add(name)

		self.routes[name] = endpoint

	def match(self, request):
		endpoint = self.routes.get(request.command)

		if endpoint is not None:
			args = endpoint.parseArgs(request.rawargs)
			return endpoint, args

		else:
			raise InvalidCommandError()

	def getRecognized(self):
		return set(self.routes.keys()) - self.sv_only
