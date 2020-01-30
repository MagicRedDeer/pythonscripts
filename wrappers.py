


def repeat(times=10):
    def dec(func):
        def _wrapper(*args, **kwargs):
            print 'in _wrapper', args, kwargs
            for i in range(times):
                func(*args, **kwargs)
            print 'back in _wrapper'
        return _wrapper
    return dec

@repeat(7)
def myfunc(*args, **kwargs):
    print 'myfunc called with args', args, kwargs


class Base(object):
    _data = None
    _sublists = None
    _additions = None

    def __init__(self):
        self._data = {}
        self._sublists = {}

    def flush(self, sublists=True):
        self._data = {}
        if sublists:
            self._sublists = {}

    @classmethod
    def flushable(cls, sublists=True):
        def wrap(func):
            def _wrapper(self, key, value):
                func(self, key, value)
                cls.flush(self, sublists=sublists)
            return _wrapper
        return wrap


class Derived(Base):

    def __init__(self):
        super(Derived, self).__init__()
        self._additions = {}
        self.populate()

    def populate(self):
        self._data.update({'name': 'World'})
        self._sublists.update({'children': ['Asia', 'Africa', 'Europe']})

    def fetch(self):
        for key, value in self._additions.items():
            if not isinstance(value, list):
                self._data[key] = value
            else:
                self._sublists[key] = value

    def getData(self):
        if not self._data:
            self.populate()
            self.fetch()
        return self._data

    def getSublists(self):
        if not self._sublists:
            self.populate()
            self.fetch()
        return self._sublists

    @Base.flushable(sublists=True)
    def add(self, key, value):
        self._additions[key] = value

    def display(self):
        print self.getData(), self.getSublists()

    def display_raw(self):
        print self._data, self._sublists


if __name__ == "__main__":
    d = Derived()
    d.display()
    d.add('parent', 'solar system')
    d.add('layers', ['atmosphere', 'crust', 'core'])
    d.display_raw()
    d.display()

