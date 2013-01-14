from purpledefrag.app.g import db
from purpledefrag.app.util import RunScore, HumanTimeDelta, phash
from datetime import datetime


class User(object):
	_autoincrement = "uid_seq"
	_key_prefix = "uid~"
	_name_index = "uname~"
	_date_fmt = "%a %d %b %Y %H:%M:%S"

	def __init__(self, name, password, lastauth = None, created = None,
		**kwargs):

		self.name = name
		self.namekey = self._name_index + name

		self.password = password
		self.lastauth = lastauth
		self.created = created

		self.__dict__.update(kwargs)

	@classmethod
	def exists(cls, name):
		return db.get(cls._name_index + name)

	@classmethod
	def getByID(cls, id):
		idkey = cls._key_prefix + str(id)
		kwargs = db.hgetall(idkey)

		if kwargs:
			kwargs["idkey"] = idkey
			kwargs["id"] = id
			return cls(kwargs.pop("name"), kwargs.pop("password"),
				**kwargs)
		else:
			return None

	@classmethod
	def findByName(cls, name):
		try:
			id = int(cls.exists(name))
		except TypeError:
			# username doesn't exist
			return None

		return cls.getByID(id)

	def authenticate(self, testpass):
		return self.password == phash(testpass)

	def setPassword(self, newpass):
		self.password = phash(newpass)
		db.hset(self.idkey, "password", self.password)

	def updateLastAuth(self):
		oldlast = self.lastauth
		self.lastauth = datetime.utcnow().strftime(self._date_fmt)
		db.hset(self.idkey, "lastauth", self.lastauth)

		return oldlast

	def create(self):
		if self.__class__.exists(self.namekey):
			raise Exception("A user named %s already exists." % self.name)

		s = db.pipeline()

		self.id = db.get(self._autoincrement)
		self.idkey = self._key_prefix + str(self.id)
		self.password = phash(self.password)
		self.lastauth = self.created = datetime.utcnow().strftime(self._date_fmt)

		stored_attributes = ("name", "password", "lastauth", "created")
		fields = dict(tuple((k, getattr(self, k)) for k in stored_attributes))

		s.hmset(self.idkey, fields)
		s.incr(self._autoincrement)
		s.set(self.namekey, self.id)

		s.execute()

class UserSession(object):
	_sess_prefix = "sess~"
	_sess_ttl = 60 * 60 * 4

	def __init__(self, ident):
		self.ident = ident
		self.sesskey = self._sess_prefix + ident

	def getUser(self):
		id = db.get(self.sesskey)

		if id:
			return User.getByID(int(id))
		else:
			return None

	def set(self, user):
		db.setex(self.sesskey, user.id, self._sess_ttl)

	def extend(self):
		db.expire(self.sesskey, self._sess_ttl)

	def remove(self):
		return db.delete(self.sesskey)

	def timeLeft(self):
		sec = db.ttl(self.sesskey) or 0
		return HumanTimeDelta(seconds = sec)

class MapRecord(object):
	def __init__(self, mapname, physics):
		self.mapname = mapname

		if physics in ("vq3", 0):
			self.promode = 0
			self.physics = "vq3"
		elif physics in ("cpm", 1):
			self.promode = 1
			self.physics = "cpm"

class RunList(MapRecord):
	_run_key = "runs:%s~%s"
	_user_run_key = "uruns:%s~%s"

	def __init__(self, mapname, physics):
		MapRecord.__init__(self, mapname, physics)
		self.runkey = self._run_key % (self.physics, mapname)

	def getRankRange(self, start, end):
		return db.zrange(self.runkey, start, end, withscores = True)

	def __getitem__(self, pos):
		try:
			s = self.getRankRange(pos, pos)[0]
		except IndexError:
			return None, None
		else:
			return s[0], RunScore(s[1])

	def __getslice__(self, start, end):
		for name, score in self.getRankRange(start, end):
			yield name, RunScore(score)

	def __len__(self):
		return int(db.zcard(self.runkey))

	def getScoreByName(self, name):
		s = db.zscore(self.runkey, name)
		if s:
			return RunScore(s)
		else:
			return None

	def getScoreByUser(self, user):
		return self.getScoreByName(user.name)

	def deleteUser(self, user):
		s = db.pipeline()
		userkey = self.makeUserKey(user, self.physics)

		s.zrem(self.runkey, user.name)
		s.zrem(userkey, self.mapname)

		s.execute()

	@classmethod
	def getUserRuns(cls, user, physics):
		userkey = cls.makeUserKey(user, physics)
		for mapname, score in db.zrange(userkey, 0, -1,
			withscores = True):
			yield cls(mapname, physics), RunScore(score)

	@classmethod
	def makeUserKey(cls, user, physics):
		return cls._user_run_key % (physics, user.id)

	def addScore(self, user, runtime):
		userkey = self.makeUserKey(user, self.physics)
		s = db.pipeline()

		s.zadd(self.runkey, runtime, user.name)
		s.zadd(userkey, runtime, self.mapname)

		s.execute()

class SpeedList(MapRecord):
	_speed_key = "speeds:%s~%s"
	_user_key = "uspeeds:%s~%s"

	def __init__(self, mapname, physics):
		MapRecord.__init__(self, mapname, physics)
		self.speedkey = self._speed_key % (self.physics, mapname)

	def addSpeedAward(self, user, speed):
		userkey = self.makeUserKey(user, self.physics)
		s = db.pipeline()

		s.zadd(self.speedkey, speed, user.name)
		s.zadd(userkey, speed, self.mapname)

		s.execute()

	def deleteUser(self, user):
		userkey = self.makeUserKey(user, self.physics)
		s = db.pipeline()

		s.zrem(self.speedkey, user.name)
		s.zrem(userkey, self.mapname)

		s.execute()

	def getBestSpeed(self):
		s = db.zrevrange(self.speedkey, 0, 0, withscores = True)
		if s:
			return s[0][0], int(s[0][1])
		else:
			return None, 0

	@classmethod
	def makeUserKey(cls, user, physics):
		return cls._user_key % (physics, user.id)

	@classmethod
	def getUserSpeeds(cls, user, physics):
		userkey = cls.makeUserKey(user, physics)
		for mapname, speed in db.zrange(userkey, 0, -1,
			withscores = True):
			yield cls(mapname, physics), int(speed)

if __name__ == "__main__":
	help(db.multi)
	z = db.incr(User._autoincrement)
	print z, type(z)
