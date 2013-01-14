g = {'cvars': {'mapname': 'hunterun-19', 'df_promode': 1} }

def extract_physic_mode(string):
    mode = -1
    parts = string.split('.')
    if parts[0] in ('cpm', 'vq3'):
        physic = parts[0]
        if len(parts) == 2:
            try:
                mode = int(parts[1])
            except ValueError:
                pass
    return physic, mode

def extract_map(args):
    if args:
        return args[0]
    return g['cvars']['mapname']

def extract_physic(args):
    mode = -1 # whats the cvar for this?! does it depend on df_promode?
    physic = g['cvars']['df_promode'] and 'cpm' or 'vq3'

    newargs = []
    for arg in args:
        if arg.startswith('cpm') or arg.startswith('vq3'):
            physic, mode = extract_physic_mode(arg)
        else:
            newargs.append(arg)

    if mode != -1:
        physic = '%s.%s' % (physic, mode)

    return physic, newargs

def count_and_remove_keyword(args, keyword):
    newargs = []
    count = 0
    for arg in args:
        if arg == keyword:
            count += 1
        else:
            newargs.append(arg)
    return count, newargs

def extract_ints(args, default):
    newargs = []
    result = default
    for arg in args:
        try:
            result = int(arg)
        except ValueError:
            newargs.append(arg)
    return result, newargs

def extract_startat(args):
    newargs = []
    startat = 1
    for arg in args:
        if arg.startswith('startat'):
            startat = int(arg.split('startat')[1])
        elif set(arg) == set('+'):
            startat += arg.count('+') * 10
        else:
            newargs.append(arg)

    return startat, newargs
