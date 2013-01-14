from urllib import FancyURLopener,urlopen
from random import choice


_user_agents = [
	"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)",
	"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
	"Mozilla/5.0 (compatible; Konqueror/2.1.1; X11)",
	"Mozilla/5.0 URL-Spider",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.153.1 Safari/525.19",
	"Mozilla/5.0 (Windows; U; Win98; en-US; rv:x.xx) Gecko/20030423 Firebird Browser/0.6"
]

class DisguisedOpener(FancyURLopener):
	def cycleUserAgents(self):
		self.addheaders[0] = ("User-Agent",choice(_user_agents))
		return self.addheaders[0][1]
		
	def open(self,*args,**kwargs):
		self.cycleUserAgents()
		return super(DisguisedOpener, self).open(*args,**kwargs)
	
	def retrieve(self,*args,**kwargs):
		self.cycleUserAgents()
		return super(DisguisedOpener, self).retrieve(*args,**kwargs)

def _inject():
	import urllib
	urllib._urlopener = DisguisedOpener()
	del urllib

if __name__ == "__main__":
	_inject()
	page = urlopen("http://defrag.co.cc/")
	page.read()
	page.close()

