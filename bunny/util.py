from datetime import timedelta
from purpledefrag.app.g import salt


class HumanTimeDelta(timedelta):
	def __str__(self):
		r = self.seconds / 60
		hours, minutes = divmod(r, 60)

		if self.days > 0:
			out = "%d days" % self.days
			if hours > 0:
				out += " and %d hours" % hours
			return out

		out = "%d minutes" % minutes
		if hours > 0:
			out = "%d hours and " % hours + out
		return out

class RunScore(int):
	'''A simple utility class to handle conversion of
	raw integer milliseconds to a human-readable time
	string
	'''

	def __str__(self):
		seconds, ms = divmod(self, 1000)
		hours, r = divmod(seconds, 3600)
		minutes, seconds = divmod(r, 60)

		h, m, s = "", "%02d:" % minutes, "%02d.%03d" % (seconds, ms)
		if hours > 0:
			h = "%02d:" % hours

		return h + m + s

def phash(plaintext):
	p = salt.copy()
	p.update(plaintext)
	return p.hexdigest()
