import sys

_s = None
def set_server(server):
    global _s
    _s = server

class Server(object):
    def __init__(self, server=None):
        self._server = server if server else _s

    def __get__(self, obj, cls=None):
        return self._server if self._server else _s

    def __set__(self, obj, server):
        self._server = server if server else _s

    def __delete__(self, obj):
        self._server = _s


class ModuleClass(object):

    _server = Server()

    def __init__(self, server=None):
        self._server = server if server else _s

    def function(self):
        print self._server
        print 'function'

    def definition(self):
        print self._server
        print 'definition'

    @classmethod
    def create(cls, server=None):
        return ModuleClass(server)


module = sys.modules[__name__]
main = ModuleClass()
for name, val in ModuleClass.__dict__.items():
    obj = getattr(main, name)
    if type(obj) == type(ModuleClass.function):
        setattr(module, name, obj)

