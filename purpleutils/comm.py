from socket import socket,AF_INET,SOCK_DGRAM
from re import compile
from time import sleep
from random import randint


class RconConnection(object):
	prefix="\xff"*4
	packet_regex=compile("%s.*?\n"%prefix)
	ascii_bytes = compile
	
	def __init__(self,server,rcon_password):
		address,port=server.split(":")
		port=int(port)
		
		self.rcon_password=rcon_password
		self.s=socket(AF_INET,SOCK_DGRAM)
		self.s.connect((address,port))
	
	def parse(self,payload):
		return payload[self.packet_regex.match(payload).end():]
	
	def send(self,payload):
		self.s.send(self.prefix + payload.encode("ascii", "ignore"))
	
	def recv(self,timeout):
		replies=[]
		
		self.s.settimeout(timeout)

		while True:
			try:
				replies.append(self.s.recv(4096))
			except:
				break
		
		return "".join(map(self.parse,replies))
	
	def command(self,command,timeout=1):
		self.send(command)
		return self.recv(timeout)
	
	def rcon(self,command,timeout=1):
		return self.command(
			"rcon \"%s\" %s"%(self.rcon_password,command),
			timeout)

	def rawclientmsg(self, clientnum, command):
		self.send("raw %d %s" % (clientnum, command))

class PurpleConnection(RconConnection):
	def rawSay(self,raw):
		return self.rcon("say "+raw)

	def broadcast(self,name,payload):
		if issubclass(type(payload),basestring):
			payload = (payload,)
		
		for segment in payload:
			if type(segment) in (float,int):
				sleep(segment)
			
			else:
				for chunk in self.wrapper.wrap(segment):
					print chunk
					self.rcon("say -n \"%s^7: %s\""%(name,chunk))

	def clientprint(self, clientnum, message):
		#self.send("rcon \"%s\" raw %d print \"%s\n\"" % (self.rcon_password, client, message))
		if len(message) > 1024:
			print "clientprint warning: raw print exceeds MAX_STRING_CHARS (=1024)"

		self.rawclientmsg(clientnum, "print \"%s\"" % message)

	def clientsay(self, clientnum, message):
		if len(message) > 150:
			print "clientsay warning: length exceeds MAX_SAY_TEXT (=150)."

		self.rawclientmsg(clientnum, "chat \"%s\"" % message)

	def clienthudprint(self, clientnum, message):
		if len(message) > 150:
			print "clienthudprint warning: length exceeds MAX_SAY_TEXT (150)"

		self.rawclientmsg(clientnum, "cp \"%s\"" % message)

class MessageSocket(object):
	def __init__(self, host, port = None):
		self.s = socket(type = SOCK_DGRAM)

		if port:
			self.s.bind((host, port))

		else:
			# allocate a random port
			while True:
				port = randint(1024, 65535)
				try:
					self.s.bind((host, port))
				except error:
					continue
				finally:
					break

		self.host = host
		self.port = port

	def listen(self):
		return self.s.recv(1024)
