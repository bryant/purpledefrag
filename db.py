class Map(object):
    @classmethod
    def get(cls, name):
        for map in maps:
            if map.name == name:
                return map
        return None

    @classmethod
    def All(cls):
        return maps

    def __init__(self, name, topspeed):
        self.name = name
        self.records = []
        self.topspeed = topspeed

    def __str__(self):
        return '<Map: %s>' % (self.name)
    def __repr__(self):
        return str(self)

class User(object):
    @classmethod
    def get(cls, name):
        for user in users:
            if user.name == name:
                return user
        return None

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.records = []

    def __str__(self):
        return '<User: %s, %s>' % (self.name, self.password)
    def __repr__(self):
        return str(self)

class Record(object):
    def __init__(self, user, map, time, mode):
        self.user = user
        self.map = map
        self.time = time
        self.mode = mode
        map.records.append(self)
        user.records.append(self)

    def __str__(self):
        return '<Record: %s [%s]- %s (%s)>' % (self.map, self.mode, self.user.name, self.time)
    def __repr__(self):
        return str(self)

users = [
    User('jesus', '1234'),
    User('bzzzz', '54321'),
    User('newbrict', '2421'),
    User('karalis', '2352'),
    User('raak', '3252'),
]

maps = [
    Map('hunterun-19', {'vq3': 900, 'cpm': 1200}),
    Map('13vast', {'vq3.2': 864, 'cpm.2': 1120}),
    Map('pornstar-slopin', {'vq3': 4102, 'cpm': 4553}),
    Map('pornstar-17percent', {}),
]

records = [
    Record(User.get('jesus'), Map.get('13vast'), '24.124', 'cpm.2'),
    Record(User.get('bzzzz'), Map.get('13vast'), '22.124', 'cpm.2'),
    Record(User.get('jesus'), Map.get('hunterun-19'), '2.124', 'cpm'),
    Record(User.get('bzzzz'), Map.get('hunterun-19'), '3.124', 'cpm'),
    Record(User.get('jesus'), Map.get('hunterun-19'), '12.124', 'vq3'),
    Record(User.get('bzzzz'), Map.get('hunterun-19'), '13.124', 'vq3'),
    Record(User.get('jesus'), Map.get('pornstar-slopin'), '26.128', 'cpm'),
    Record(User.get('newbrict'), Map.get('pornstar-slopin'), '26.256', 'cpm'),
    Record(User.get('bzzzz'), Map.get('pornstar-slopin'), '26.240', 'cpm'),
    Record(User.get('karalis'), Map.get('pornstar-slopin'), '29.240', 'cpm'),
    Record(User.get('raak'), Map.get('pornstar-slopin'), '41.240', 'cpm'),
    Record(User.get('jesus'), Map.get('pornstar-slopin'), '29.480', 'vq3'),
    Record(User.get('bzzzz'), Map.get('pornstar-slopin'), '27.016', 'vq3'),
    Record(User.get('newbrict'), Map.get('pornstar-slopin'), '28.112', 'vq3'),
    Record(User.get('karalis'), Map.get('pornstar-slopin'), '41.240', 'vq3'),
    Record(User.get('raak'), Map.get('pornstar-slopin'), '45.240', 'vq3'),
]


