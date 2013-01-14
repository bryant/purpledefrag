'''from urllib import urlopen
#from BeautifulSoup import BeautifulSoup
from xml.dom.minidom import parseString
from sys import argv


u = urlopen('http://q3a.ath.cx/?map=%s&fo=2&show=100'%"test")
src = u.read()
u.close()

start = src.find("<table id=\"mview0\"")
end = src.find("</table>",start)+len("</table>")

#rawtable = BeautifulSoup(src[start:end])

doc = parseString(src[start:end].replace("\n",""))
results = []

for row in doc.getElementsByTagName("tr")[1:]:
	print dir(row.getElementsByTagName("td")[3])
'''

from BeautifulSoup import BeautifulSoup
from re import compile, DOTALL
from urllib import quote
from .useragentlib import DisguisedOpener


class Q3DFRecords(object):
	delim = compile(r"<tbody>(.*?)</tbody>",DOTALL)

	def __init__(self,
		cpmfmt = "http://www.q3df.org/rankings/map-%s/sort-rank/asc/physic-1",
		vq3fmt = "http://www.q3df.org/rankings/map-%s/sort-rank/asc/physic-0",
		cpmctffmt = "http://www.q3df.org/rankings/map-%s/sort-rank/asc/physic-2",
		vq3ctffmt = "http://www.q3df.org/rankings/map-%s/sort-rank/asc/physic-3"):

		self.cpm = cpmfmt
		self.vq3 = vq3fmt
		self.cpmctf = cpmctffmt
		self.vq3ctf = vq3ctffmt

	def ripTopRow(self,raw):
		firstrow = BeautifulSoup(raw,
			convertEntities = BeautifulSoup.HTML_ENTITIES).tr
		if firstrow is None:
			return None

		cols = firstrow("td", {"class":compile("^bg2")})
		if len(cols) != 6:
			return None

		return dict(zip(
			("date","owner","runtime"),
			(stripHTML(col) for col in cols[:3])
		))
	
	def grabAndMatch(self,url):
		try:
			page = urlopen(url)
		except:
			return None
		else:
			match = self.delim.search(page.read())
			page.close()

			if match is None:
				return None

			return self.ripTopRow(match.group(1))

	def getBestCPM(self,mapname):
		mapname = quote(mapname)
		match = self.grabAndMatch(self.cpm % mapname) or \
			self.grabAndMatch(self.cpmctf % mapname)

		if match is not None:
			match["physics"] = "cpm"
		return match
	
	def getBestVQ3(self,mapname):
		mapname = quote(mapname)
		match = self.grabAndMatch(self.vq3 % mapname) or \
			self.grabAndMatch(self.vq3ctf % mapname)

		if match is not None:
			match["physics"] = "vq3"
		return match

	def testUserAgent(self):
		page = urlopen("http://defrag.co.cc/")
		page.read()
		page.close()

def stripHTML(soupobj):
	text = "".join(soupobj(text = True)).strip()
	return text.replace("^","^^7")

def getBest(mapname,promode = 1):
	if type(promode) is not int:
		if promode.lower() == "vq3":
			promode = 0
		else:
			promode = 1
	
	if promode == 1:
		print "getBest:",mapname
		return _q3df.getBestCPM(mapname)
	else:
		return _q3df.getBestVQ3(mapname)

_q3df = Q3DFRecords()


if __name__ == "__main__":
	# Q3DFRecords(None,None).testUserAgent()
	print Q3DFRecords().getBestVQ3("icepoint")

