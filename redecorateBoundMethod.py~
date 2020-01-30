def summer(func):
    def _wrapper(*args, **kwargs):
        return sum(func(*args, **kwargs))
    _wrapper.__doc__ = func.__doc__
    return _wrapper

class MyClass(object):

    """Docstring for MyClass. """

    def __init__(self):
        """TODO: to be defined1. """

    @summer
    def method1(self):
        '''method1 documentation'''
        return range(10)

    def method2(self):
        '''method2 documentation'''
        return range(20)

    def method3(self):
        '''method3 documentation'''
        return range(30)

MyClass.method2 = summer(MyClass.method2)
MyClass.backup = MyClass.method3

if __name__ == "__main__":
    c = MyClass()
    c.method3 = summer(c.method3)
    help(c.method1)
    help(c.method2)
    print c.method1()
    print c.method2()
    print c.method3()
    print c.backup()
