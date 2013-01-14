from purpledefrag.app.controllers.base import *


def lastmap(request):
	return ConsoleResponse("^6Last map is sago. Last map is always sago. Bunny lufs sago.")

def mapinfo(request):
	return ConsoleResponse("^6Map info goes heeyah.")

def newmaps(request):
	return ConsoleResponse("^5Purple text is kinda gey.\nHere be narwhals!\nMormon porn rulez.")

def maprequest(request):
	return ConsoleResponse("^5X is an invalid map, ignoring your spam suckah")

class MapInfoController(BaseController):
	opt = PurpleArgParser(prog = "/mapinfo")

	def command(self):
		text = "^5The current map is \'%s\'" % g.cvars["mapname"]
		return ConsoleResponse(text)

class RandomMapController(BaseController):
	opt = PurpleArgParser(prog = "/random", add_help = True)
	opt.add_argument("search_term", nargs = "?",
		help = "Find maps with names containing this word",
		default = None)

	def command(self):
		maps = g.maps.getRandom(8, self.args.search_term)
		return ConsoleResponse("^5%d maps:\n%s" % (len(maps), "\n".join(maps)))
