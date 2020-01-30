class MyClass(object):

    def __init__(self):
        self.member = 'i am a member'

    def __setattr__(self, name, val):
        if hasattr(self, name):
            super(MyClass, self).__setattr__(name, val)
        print 'setattr called', self, self.__class__, name

    def __getattribute__(self, name):
        return super(MyClass, self).__getattribute__(name)
        print 'getattr called', self, self.__class__, name

cl = MyClass()
cl.member = 'hello there'
cl.non_member = 6
print cl.member
print cl.non_me
