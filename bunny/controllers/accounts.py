from purpledefrag.app.controllers.base import *
from purpledefrag.app.models import *
from purpledefrag.exceptions import ArgError
from purpledefrag.q3df.q3df import getBest
from purpledefrag import BunnyResponse, HUDResponse
from re import compile
from itertools import izip


class LoginController(BaseController):
	opt = PurpleArgParser(prog = "/login",
		description = "Login with your current name, or a chosen username",
		epilog = "Example: /login my_secret_password")
	opt.add_argument(
		"--username", dest = "u", metavar = "USERNAME", type = str,
		help =
			"Use USERNAME as your login name instead "
			"of your current game name."
	)
	opt.add_argument(
		"p", metavar = "password", type = str,
	)

	def command(self):
		session = UserSession(self.request.client)
		if session.getUser() is not None:
			session.extend()

			return ConsoleResponse(
				"^6You're already logged in for the next ^2%s" %
				session.timeLeft()
			)

		username = self.args.u or self.request.name
		user = User.findByName(username)

		if not user or not user.authenticate(self.args.p):
			print "Bad password for [%s], [%s]" % (username, self.args.p)
			return ConsoleResponse("^1Incorrect login credentials.")
		else:
			print "Authenticated", username
			session.set(user)

			return ConsoleResponse(
				"^2Welcome back, ^7%s^2.\n"
				"Last login was on %s UTC.\n"
				"Time left on this session: %s.\n"
				"^3Log out with /logout" %
				(user.name, user.updateLastAuth(), session.timeLeft())
			)

class LogoutController(BaseController):
	opt = PurpleArgParser(prog = "/logout")

	def command(self):
		session = UserSession(self.request.client)
		user = session.getUser()
		session.remove()

		if user:
			return ConsoleResponse(
				"^5You've been logged out.\n"
				"Your username was ^7%s^5.\n"
				"When you come back, use ^7/name %s; /login [your password]^5 to log back in." %
				(user.name, user.name)
			)
		else:
			return ConsoleResponse("^5Logged out. Log back in with /login")

class RegistrationController(BaseController):
	opt = PurpleArgParser(prog = "/register",
		description = "Register an account with your current gamename",
		epilog = "Example: /register my_secret_password")
	opt.add_argument(
		"--username", dest = "u", metavar = "USERNAME", type = str,
		help = "Register the name USERNAME instead of the name you're using in-game."
	)
	opt.add_argument(
		"p", metavar = "password", type = str,
		help = "The password you want"
	)

	_maxlen = 32

	def command(self):
		username = self.args.u or self.request.name

		if len(username) > self._maxlen or len(self.args.p) > self._maxlen:
			return ConsoleResponse(
				"Username and password cannot be longer than %d characters." %
				self._maxlen
			)

		if User.exists(username):
			return ConsoleResponse(
				"^1'%s' has already been taken by someone else. Choose another." %
				username
			)

		user = User(username, self.args.p,
			ip = self.request.ip)
		user.create()
		UserSession(self.request.client).set(user)

		return ConsoleResponse(
			"^6Congrats! You are signed in as '^2%s^6'.\n"
			"Your password is ^1%s^6 -- keep it safe!" %
			(user.name, self.args.p)
		)

class WhoController(BaseController):
	opt = PurpleArgParser(prog = "/WhoAmI")

	def command(self):
		session = UserSession(self.request.client)
		user = session.getUser()

		if user:
			return ConsoleResponse(
				"^6You are logged in as ^7%s^6. Your session expires in ^3%s^6." %
				(user.name, session.timeLeft())
			)
		else:
			return ConsoleResponse("^1You have not signed in.")

class RankingsController(BaseController):
	opt = PurpleArgParser(prog = "/top", add_help = True)
	opt.add_argument("-p", type = int, default = None,
		dest = "physics", choices = (1, 0), help = "1 = CPM, 0 = VQ3")
	opt.add_argument("-s", type = int, default = 0)
	opt.add_argument("map", nargs = "?", default = None,
		help = "Name of a map. Leave it out for the current one.")

	def prettyTable(self, scores, start = 0):
		out = ""
		for rank, (name, score) in izip(xrange(start + 1, start + 11),
			scores[start:start + 10]):

			out += "^7%-3d^5" % rank + str(score) + "^4..."
			out += "^7" + name + "^5\n"

		return out

	def command(self):
		mapname = self.args.map or g.cvars["mapname"]
		physics = self.args.physics or int(g.cvars["df_promode"])

		map = RunList(mapname, physics)

		return ConsoleResponse(
			"^2Top runs for %s (%s):\n%s" %
			(mapname, map.physics, self.prettyTable(map, self.args.s))
		)

class SpeedRankingsController(BaseController):
	opt = PurpleArgParser(prog = "/topspeed", add_help = True)
	opt.add_argument("--physics", type = int, default = None,
		choices = (1, 0), help = "1 = CPM, 0 = VQ3")
	opt.add_argument("map", nargs = "?", default = None)

	def command(self):
		mapname = self.args.map or g.cvars["mapname"]
		physics = self.args.physics or int(g.cvars["df_promode"])
		map = SpeedList(mapname, physics)
		name, bestspeed = map.getBestSpeed()

		if bestspeed:
			return ConsoleResponse(
				"^2Top speed for %s (%s): ^5%s ups / ^7%s" %
				(mapname, map.physics, bestspeed, name)
			)
		else:
			return ConsoleResponse("^2Top %s speed for %s: dust." %
				(map.physics, mapname))

class BestTimeController(BaseController):
	opt = PurpleArgParser(prog = "/mytop")
	opt.add_argument("--physics", type = int, default = None,
		choices = (1, 0), help = "1 = CPM, 0 = VQ3")
	opt.add_argument("map", nargs = "?", default = None,
		help = "Name of a map. Leave it out for the current one.")

	def command(self):
		user = UserSession(self.request.client).getUser()

		if user:
			physics = self.args.physics or int(g.cvars["df_promode"])
			mapname = self.args.map or g.cvars["mapname"]
			score = RunList(mapname, physics).getScoreByUser(user)

			if score:
				return BunnyResponse("^7%s's ^2best time on ^3%s^2 is ^5%s" %
					(user.name, mapname, score),
					clientnum = -1)
			else:
				return BunnyResponse("^7%s ^2has never done ^3%s" %
					(user.name, mapname),
					clientnum = -1)
		else:
			return ConsoleResponse(
				"^3OH NOES! Bunny can't keep track of your "
				"scores because you have no account! Quick, "
				"type ^2/register^3 and start hopping!"
			)

class FinishLineController(BaseController):
	_server_only = True
	_df_regex = compile(
		"^ClientTimerStop: (?P<clientnum>[0-9]+) (?P<ms>[0-9]+) "
		"\"(?P<map>[^\"]+)\" \"(?P<owner>[^\"]*)\" (?P<gametype>[0-9\-]+) "
		"(?P<promode>[0-9]+) (?P<mode>[0-9\-]+) (?P<interference>[0-9]+) "
		"(?P<ob>[0-9]+) (?P<version>[0-9]+) (?P<date>[0-9\-]+)"
	)

	@classmethod
	def parseArgs(cls, raw):
		match = cls._df_regex.match(raw)

		if match is not None:
			args = match.groupdict()
			for k in ("interference", "mode", "ms", "gametype",
				"promode","ob"):
				args[k] = int(args[k])

			return args

		else:
			raise ArgError("Could not parse [%s]" % raw)

	def invalidConditions(self):
		args = self.args

		if args["interference"] != 3:
			return (
				"This run doesn't count because interference "
				"is on. /callvote interference 3"
			)
		elif args["mode"] in (5, 6, 7):
			return "This run wasn't counted. Mode must not be 5, 6, or 7. /callvote mode to remedy this."
		
		return None

	def command(self):
		invalid = self.invalidConditions()

		if invalid:
			return ConsoleResponse("^1" + invalid)
		else:
			args = self.args
			session = UserSession(self.request.client)
			user = session.getUser()

			if user is not None:
				map = RunList(args["map"], args["promode"])
				curr_score = map.getScoreByUser(user)

				if curr_score is None or args["ms"] < curr_score:
					map.addScore(user, args["ms"])

				#extend his session some more
				session.extend()

			else:
				return ConsoleResponse(
					"defra^5y ^2b^7unny^7: ^2Nice time! But you weren't logged in, or "
					"you don't have an account. Type ^7/login^2 "
					"or ^7/register [password]^2 :)"
				)

class LoginReminderController(BaseController):
	_server_only = True

	@classmethod
	def parseArgs(cls, raw):
		return dict()

	def command(self):
		sess = UserSession(self.request.client)
		user = sess.getUser()

		if user:
			return ConsoleResponse(
				"^2Logged in as ^7%s^2 for the next ^7%s" %
				(user.name, sess.timeLeft())
			)
		else:
			return BunnyResponse(
				"Just a reminder, %s^2, that you haven't logged in yet." %
				self.request.name
			)
			

class SpeedAwardController(BaseController):
	_server_only = True
	_df_regex = compile(
		"^ClientSpeedAward: (?P<clientnum>[0-9]+) (?P<speed>[0-9]+) "
	)

	@classmethod
	def parseArgs(cls, raw):
		match = cls._df_regex.match(raw)

		if match is not None:
			args = match.groupdict()
			args["speed"] = int(args["speed"])

			return args

		else:
			raise ArgError("SpeedAwardController could not parse [%s]" % raw)

	def command(self):
		speed = self.args["speed"]
		session = UserSession(self.request.client)
		user = session.getUser()

		if user is not None:
			map = SpeedList(g.cvars["mapname"], int(g.cvars["df_promode"]))
			map.addSpeedAward(user, speed)

			session.extend()

class WorldRecordController(BaseController):
	opt = PurpleArgParser(prog = "/wr")
	opt.add_argument("-p", type = int, default = None, choices = (0, 1),
		help = "1 = CPM, 0 = VQ3")
	opt.add_argument("mapname", nargs = "?", default = None)

	def command(self):
		mapname = self.args.mapname or g.cvars["mapname"]

		if self.args.p is not None:
			promode = self.args.p
		else:
			promode = int(g.cvars["df_promode"])

		physics = ("vq3", "cpm")[promode]
		key = "wrcache:%s~%s" % (physics, mapname)
		ret = g.db.get(key)

		if not ret:
			r = getBest(mapname, promode)
			if r:
				ret = (
					"^5%s world record (%s): ^7%s^5 by %s" %
					(mapname, physics, r["runtime"], r["owner"])
				)
			else:
				ret = "No %s record for %s" % (physics, mapname)

			g.db.setex(key, ret, 60 * 60 * 24)

		return ConsoleResponse(ret)
