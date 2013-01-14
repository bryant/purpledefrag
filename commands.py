import lxml
import urllib
from router import route
from db import Map, User, Record
from utils import extract_physic, extract_physic_mode, extract_startat, \
    count_and_remove_keyword, extract_ints, extract_map


@route
def user(request):
    user_actions = '''name stats time timehistory times besttimes worsttimes
    elo elopos bestranks worstranks mostplayed leastplayed
    mostimproved leastimproves recentbeaten tiedranks pos alias'''.split()

    args = request.args
    show, args = count_and_remove_keyword(args, 'show')
    actions = set()
    for action in user_actions:
        num, args = count_and_remove_keyword(args, action)
        if num:
            actions.add(action)
    startat, args = extract_startat(args)
    physic, args = extract_physic(args)

    if args:
        user = args[0]
    else:
        user = 'CURRENT_USER'

    mapname = extract_map(args[1:])

    return actions, 'for', user, 'onmap', mapname, physic

@route
def timehistory(request):
    request.args.append('timehistory')
    return user(request)

@route
def time(request):
    request.args.append('time')
    return user(request)

@route
def wr(request):
    args = request.args
    show, args = count_and_remove_keyword(args, 'show')
    physic, args = extract_physic(args)
    mapname = extract_map(args)

    physic, mode = extract_physic_mode(physic)
    physic = {'cpm': 1, 'vq3': 0}[physic]

    return mapname, physic, mode

    getmapurl = 'http://www.q3df.org/records/details?map=%s&mode=%s&physic=%i'
    data = urllib.urlopen(getmapurl % (mapname, mode, physic)).read()
    doc = lxml.html.document_fromstring(data)
    results = []
    for tr in doc.xpath('//table//tr'):
        if len(tr.xpath('td')) != 6:
            continue
        date, player, time, rank, physic, server = [x.text_content() for
                                                    x in tr.xpath('td')]
        results.append((time, player.strip()))
    return results


@route
def random(request):
    args = request.args
    show, args = count_and_remove_keyword(args, 'show')
    #ctf, args = count_and_remove_keyword(args, 'ctf')

    string = ''
    if args:
        string = args[0]

    result = []
    for map in Map.All():
        if string in map.name:
            result.append(map)
    return result[:5]

@route
def topspeed(request):
    args = request.args
    show, args = count_and_remove_keyword(args, 'show')
    physic, args = extract_physic(args)
    mapname = extract_map(args)

    map = Map.get(mapname)
    topspeed = 'dust'
    if map:
        if physic in map.topspeed:
            topspeed = map.topspeed[physic]
    return topspeed


@route
def login(request):
    if len(request.args) == 2:
        username, password = request.args
    elif len(request.args) == 1:
        username = request.name
        password = request.args[0]
    return 'Logging in', username, password


#def pr(mapphysic=CurrentMap(), show=False, combined=False, startat=Pager()):
@route
def pr(request):
    args = request.args
    show, args = count_and_remove_keyword(args, 'show')
    combined, args = count_and_remove_keyword(args, 'combined')
    startat, args = extract_startat(args)
    physic, args = extract_physic(args)
    mapname = extract_map(args)

    if show: print 'SHOWING'
    if combined: print 'COMBINED'
    print 'STARTAT', startat
    print 'MAP', mapname, physic

    map = Map.get(mapname)
    if not map:
        return []
    result = []
    for record in map.records:
        if record.mode == physic:
            result.append((record.time, record.user.name))
    return sorted(result)


@route
def setpass(request):
    user = User.get('jesus')
    user.password = request.args[0]
    return user


@route
def rank(request):
    args = request.args
    show, args = count_and_remove_keyword(args, 'show')
    number, args = extract_ints(args, 1)
    physic, args = extract_physic(args)
    mapname = extract_map(args)
    if show: print 'SHOWING'
    print 'NUMBER', number

    map = Map.get(mapname)
    result = []
    for record in map.records:
        if record.mode == physic:
            result.append(record)
    if len(result) < number:
        return None
    return result[number-1]

@route
def arca(request):
    return rank(request)

@route
def gay(request):
    return rank(request)
