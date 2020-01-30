class Base1(object):
    def __init__(self):
        print 'Base 1 init'

class Base2(object):
    def __init__(self):
        print 'Base 2 init'

class Child(Base1, Base2):
    def __init__(self):
        Base1.__init__(self)
        Base2.__init__(self)

if __name__ == '__main__':
    child = Child()
