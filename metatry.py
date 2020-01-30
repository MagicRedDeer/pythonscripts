class Meta(type):

    instances = {}

    def __init__(self, *args, **kwargs):
        print 'Meta created', id(self)

    def __new__(cls, name, bases, dct):
        print 'meta new', cls, name, bases, dct.keys()
        newdct = {}
        for key, value in dct.items():
            key = key.upper()
            newdct[key] = value
        dct.update(newdct)
        return super(Meta, cls).__new__(cls, name, bases, dct)

    def __call__(self, *args, **kwargs):
        key = ((self.__module__ + '.')
               if hasattr(self, '__module__') else '') + self.__name__
        print ('meta __call__ called', self, args, kwargs, 'key=', key,
               self.__name__)
        if key in self.instances:
            return self.instances.get(key)
        obj = super(Meta, self).__call__(*args, **kwargs)
        self.instances[key] = obj
        return obj


class Singleton(object):
    __metaclass__ = Meta

    myAttr = 1

    def __init__(self):
        print 'object created'

    def myFunc(self):
        print 'myFunc called'

    print 'class definition'


class AnotherSingleton(object):
    __metaclass__ = Meta

    def __init__(self):
        print 'another object created'

    def myFunc(self):
        print 'another myFunc called'

    print 'another class definition'


if __name__ == "__main__":
    c = Singleton()
    c.MYFUNC()
    c.myFunc()
    d = Singleton()

    print id(c), id(d)

    a = AnotherSingleton()
    b = AnotherSingleton()
    print id(a), id(b)
