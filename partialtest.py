import functools


def greeting(arg1, arg2='Hello'):
    print arg2, arg1

bye = functools.partial(greeting, arg2='Goodbye')


class Greetings(object):

    def __init__(self, greeting='Hello'):
        self.greeting = greeting

    def greet(self, name='John'):
        print self.greeting, name

    greetJohn = functools.partial(greet, name='John')


if __name__ == "__main__":
    print '%(a)s_%(a)s' % {'a':'Allo'}
