import functools


class C(object):
    _a = 'a'
    _b = 'b'

    def get_a(self):
        return self._a

    def set_a(self, value):
        self._a = value
    a = property(fget=get_a, fset=set_a)

    def get_b(self):
        return self._b

    def set_b(self, value):
        self._b = value
    b = property(fget=get_b, fset=set_b)


class FuncOverride(object):

    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__
        self.__name__ = func.__name__

    def __get__(self, obj, cls):
        func = self.func

        def _func(*args, **kwargs):
            return func(obj.c, *args, **kwargs)
        _func.__doc__ = self.func.__doc__
        _func.__name__ = self.func.__name__

        return _func


class B(C):

    def __init__(self, c):
        self.c = c

    a_setter = FuncOverride(C.set_a)
    a_getter = FuncOverride(C.get_a)
    b_setter = FuncOverride(C.set_b)
    b_getter = FuncOverride(C.get_b)

if __name__ == "__main__":
    c = C()
    b = B(c)
    c.a = '_a'
    print b.a_getter()
