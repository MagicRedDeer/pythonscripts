import abc


from weakref import WeakSet


class Base(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def prop(self):
        return 0

    def method(self):
        print 'method', id(self), 'called'


class Derived(Base):

    def method(self):
        return super(Derived, self).method()




Derived.register(long)
Derived.register(float)


if __name__ == "__main__":
    print isinstance(1, Derived)
    Derived._dump_registry()
    obj = Derived()
    print obj.prop
    print obj.method()
