class ArgError(Exception):
	pass

class PurpleArgError(ArgError):
	def __init__(self, message):
		self.message = message

class InvalidCommandError(Exception):
	pass
