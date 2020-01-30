import random


class List(list):
    minn = 0
    maxx = 100


class Prop(object):
    def __init__(self, maxx=None):
        self._lists = {}
        try:
            self.maxx = int(maxx)
        except (TypeError, ValueError):
            self.maxx = 0

    def __get__(self, instance, owner):
        i = id(instance)
        if i in self._lists:
            r = self._lists.get(i)
        else:
            start = random.randint(0, self.maxx)
            end = random.randint(start, self.maxx + 1)
            r = range(start, end)
            self._lists[i] = r
        return r

    def __set__(self, instance, value):
        self._lists[id(instance)] = value

    def __del__(self, instance):
        i = id(instance)
        if i in self._lists:
            del self._lists[i]


class PropParams(object):
    def __init__(self, prop, maxx=10):
        self.prop = prop
        print prop
        self.prop.maxx = maxx

    def setMaxx(self, maxx=10):
        self.prop.maxx = maxx


class Object(object):

    prop1 = Prop()
    prop1_params = PropParams(prop1)
    prop2 = Prop()

    def __init__(self):
        print 'Object created', id(self)


if __name__ == "__main__":
    obj = Object()
    print obj.prop1, obj.prop2
    print obj.prop1, obj.prop2

    obj2 = Object()
    obj2.prop1 = [1, 2]
    obj2.prop2 = [3, 7]
    print obj2.prop1, obj2.prop2
    print obj2.prop1, obj2.prop2

    print type(obj2), getattr(type(obj2), 'prop1')
