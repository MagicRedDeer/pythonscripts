

class Params(dict):

    _prop = None
    _instance = None

    def getProp(self):
        return self._prop
    def setProp(self, prop):
        self._prop = prop
    def getInstance(self):
        return self._instance
    def setInstance(self, instance):
        self._instance = instance
        if self._prop:
            self._prop._params[id(instance)]=self

    def copy(self):
        d = Params(super(Params, self).copy())
        d.setProp(self.getProp())
        return d


class Desc(object):

    _default_params = None
    _params = None

    def __init__(self, params=None):
        if params is None:
            params = Params()
        params.setProp(self)
        self._default_params = params
        self._params = {}

    def __get__(self, instance, owner):
        items = self._params[id(instance)].items()
        return reduce(lambda x, y: x+y, map(lambda item: item[0]*item[1], items), 0)

class Meta(type):

    def __new__(cls, name, bases, dct):
        for key, value in dct.items():
            if isinstance(value, Desc):
                dct[key+'Params']=value._default_params
        return super(Meta, cls).__new__(cls, name, bases, dct)


class MyClass(object):
    'don\'t try this at home '

    __metaclass__ = Meta

    d = Desc(Params({1:1}))

    def __init__(self):

        for attr_name in dir(self):
            if attr_name.endswith('Params'):
                attr = getattr(self, attr_name)
                if isinstance(attr, Params):
                    newattr = attr.copy()
                    newattr.setInstance(self)
                    setattr(self, attr_name, newattr)

if __name__ == "__main__":
    c = MyClass()
    print c.d
    c.dParams[2] = 2
    print c.d
    d = MyClass()
    d.dParams[3] = 1
    print c.d
    print d.d



