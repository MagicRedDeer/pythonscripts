
class Meta(type):

    def __new__(cls, name, bases, dct):
        dct['memParams'] = {'old': 1}
        return super(cls, Meta).__new__(cls, name, bases, dct)

class A(object):
    __metaclass__ = Meta
    mem = None

    def __init__(self):
        self.memParams = {'new': 1}


a = A()
print a.memParams, A.memParams



