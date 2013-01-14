from purpledefrag.app.app import PurpleApp
from purpledefrag.app.controllers import routes
from sys import argv
import purpledefrag.app.g as g


if __name__ == "__main__":
	g.initCDict(argv[1])
	maplist = g.maps

	host = "localhost:" + g.cvars["net_port"]
	print "Server to", host
	app = PurpleApp(host, g.cvars["rconPassword"], routes)
	print "Updating map list"
	print "Got %d maps" % maplist.updateList(app.server)

	msgs = app.messages
	app.notify()
	print "Listening on %s:%d" % (msgs.host, msgs.port)
	app.serveForever()
