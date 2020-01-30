from __future__ import print_function
import functools
import collections
import ipdb


class memoize(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        ipdb.set_trace()
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


@memoize
def fib_memo(n):
    if n <= 1:
        return n
    else:
        return fib_memo(n - 1) + fib_memo(n - 2)


if __name__ == "__main__":
    import timeit
    nomem = (timeit.timeit('fib(25)',
                           setup='from decorator_test import fib',
                           number=10))
    mem = (timeit.timeit('fib_memo(25)',
                         setup='from decorator_test import fib_memo',
                         number=10))
    print (nomem, mem, nomem/mem)
