

class desc(object):

    def __init__(self, initval):
        self.initval = initval
        self.val = None

    def __get__(self, obj, cls=None):
        print id(self)
        return self.val if self.val else self.initval

    def __set__(self, obj, val):
        self.val = val



class Holder(object):

    mydesc = desc(1)


if __name__ == "__main__":
    h1 = Holder()
    h2 = Holder()
    print h1.mydesc
    h1.mydesc = 7
    print h1.mydesc
    print h2.mydesc
