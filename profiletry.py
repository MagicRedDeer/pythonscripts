import tempfile
import cProfile

def profile(sort='cumulative', lines=50, strip_dirs=False):
    """A decorator which profiles a callable.
    Example usage:

    >>> @profile
        def factorial(n):
            n = abs(int(n))
            if n < 1:
                    n = 1
            x = 1
            for i in range(1, n + 1):
                    x = i * x
            return x
    ...
    >>> factorial(5)
    Thu Jul 15 20:58:21 2010    /tmp/tmpIDejr5

             4 function calls in 0.000 CPU seconds

       Ordered by: internal time, call count

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 profiler.py:120(factorial)
            1    0.000    0.000    0.000    0.000 {range}
            1    0.000    0.000    0.000    0.000 {abs}

    120
    >>>
    """
    def outer(fun):
        def inner(*args, **kwargs):
            file = tempfile.NamedTemporaryFile(delete=False)
            prof = cProfile.Profile()
            try:
                ret = prof.runcall(fun, *args, **kwargs)
            except:
                file.close()
                raise

            prof.print_stats()
            with open('somefile', 'w+') as f:
                prof.dump_stats(f)
            # stats = pstats.Stats(file.name)
            # if strip_dirs:
            #     stats.strip_dirs()
            # if isinstance(sort, (tuple, list)):
            #     stats.sort_stats(*sort)
            # else:
            #     stats.sort_stats(sort)
            # stats.print_stats(lines)

            return ret
        return inner

    # in case this is defined as "@profile" instead of "@profile()"
    if hasattr(sort, '__call__'):
        fun = sort
        sort = 'cumulative'
        outer = outer(fun)
    return outer

def fib(x):
    if x <= 2:
        return 1
    else:
        return fib(x-1)+fib(x-2)

@profile
def callfib():
    return fib(20)

if __name__ == '__main__':
    callfib()

