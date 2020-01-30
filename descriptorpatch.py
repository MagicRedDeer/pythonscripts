
# A demonstration that descriptor cannot be patched at instance level

import pprint


class Desc(object):

    def __init__(self, value):
        self._value = value

    def __get__(self, obj, cls):
        return getattr(obj, '_value', None) or self._value

    def __set__(self, obj, value):
        obj._value = value


class A(object):
    desc1 = Desc(1)

A.desc2 = Desc(2)


if __name__ == "__main__":
    a = A()
    A.desc3 = Desc(3)
    a.desc4 = Desc(4)

    pprint.pprint(A.__dict__)
    pprint.pprint(a.__dict__)
    print a.desc1, a.desc2, a.desc3, a.desc4
