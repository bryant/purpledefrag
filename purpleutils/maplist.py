from re import compile, MULTILINE
from random import sample


class MapList(object):
	map_delimiter=compile("^(\\S+?)\\.bsp", MULTILINE)
	data_start=compile(".*?\n---------------\n")

	def updateList(self, server):
		self.maps = set(self.rawToList(server.rcon("dir maps bsp")))
		return len(self.maps)

	def rawToList(self, raw):
		data = raw[self.data_start.match(raw).end():]
		return sorted((m.lower() for m in self.map_delimiter.findall(data)))

	def getRandom(self, count, searchterm = None):
		pool = self.maps
		if searchterm is not None:
			search = searchterm.lower()
			pool = filter(lambda x: search in x, self.maps)

		if len(pool) > count:
			pool = sample(pool, count)

		return pool
