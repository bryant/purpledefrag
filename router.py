
routes = {}

def route(f):
    def wrap(request):
        return f(request)
    routes[f.func_name] = wrap
    return wrap












