
def affects(*crargs):
    def decorator(func):
        def wrapper(*args):
            for arg in crargs:
                print 'securing', arg
            result = func(*args)
            for arg in crargs:
                print 'exposing', arg
            return result
        return wrapper
    return decorator


class MyClass(object):

    #@affects('area1', 'function1')
    def mymethod(self):
        print "MyClass.mymethod called"
    mymethod = affects('area1', 'function1')(mymethod)

if __name__ == '__main__':
    cl = MyClass()
    cl.mymethod()
