from purpledefrag import CvarDict, Map, MapList, BunnyResponse
from redis import Redis
from hashlib import sha256


class GentleReminder(Map):
	def match(self, request):
		if request.command.startswith('!') and \
			"reminder" in self.routes:
			return self.routes["reminder"], None

		return Map.match(self, request)

	def getRecognized(self):
		k = Map.getRecognized(self)
		return k - set(("reminder",))

def initCDict(pid):
	global cvars
	cvars = CvarDict("/openarena:" + pid)

cvars = None
routes = GentleReminder()
maps = MapList()
db = Redis(host = "localhost", port = 6379, db = 0)
salt = sha256("your salt here")
