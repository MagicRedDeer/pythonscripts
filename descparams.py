import random


class DescParams(dict):

    _prop = None
    _instance = None

    def __init__(self, *args, **kwargs):
        super(DescParams, self).__init__(*args, **kwargs)

    def __setitem__(self, i, value):
        self._clearInstanceCache()
        super(DescParams, self).__setitem__(i, value)

    def _setProp(self, prop):
        self._prop = prop

    def _setInstance(self, instance):
        self._instance = instance
        if self._prop:
            self._prop._params[id(instance)]=self

    def copy(self):
        _new = DescParams(super(DescParams, self).copy())
        if self._prop:
            _new._setProp(self._prop)
        if self._instance:
            _new._setInstance(self._instance)
        return _new

    def _clearInstanceCache(self):
        if self._prop and self._instance:
            d = self._prop._lists
            if d.has_key(id(self._instance)):
                del self._prop._lists[ id(self._instance) ]


class ListDesc(object):

    _default_params = None
    _params = None
    _lists = None

    def __init__(self, params):
        self._default_params = params
        self._default_params._setProp(self)
        self._lists = {}
        self._params = {}

    def __get__(self, instance, owner):

        if self._lists.has_key(id(instance)):
            return self._lists.get(id(instance))
        else:
            minn = self._params[id(instance)]['minn']
            maxx = self._params[id(instance)]['maxx']
            arr = range(minn, maxx)
            self._lists[id(instance)] = arr
            return arr


class Meta(type):

    def  __new__(cls, name, bases, dct):
        newdct = dct.copy()
        for k, v in dct.items():
            if isinstance(v, ListDesc):
                newdct[k+'Params'] = v._default_params
        return super(Meta, cls).__new__(cls, name, bases, newdct)

    def __call__(self):
        print 'call', self, type(self)
        return super(Meta, self).__call__()

class MyClass(object):

    __metaclass__ = Meta
    prop = ListDesc(DescParams({ 'maxx': 20, 'minn': 0 }))
    prop2 = ListDesc(DescParams({ 'maxx': 10, 'minn': 0 }))

    def __init__(self):
        print 'init myclass', self
        for attr_name in dir(self):
            if attr_name.endswith('Params'):
                attr = getattr(self, attr_name)
                if isinstance(attr, DescParams):
                    newattr = attr.copy()
                    newattr._setInstance(self)
                    setattr(self, attr_name, newattr)


if __name__ == "__main__":

    c = MyClass()
    d = MyClass()
    print c.prop
    print d.prop
    print c.prop2
    print d.prop2
    c.prop2Params[ 'maxx' ] = 7
    d.prop2Params[ 'minn' ] = 7
    print c.prop
    print d.prop
    print c.prop2
    print d.prop2

