class Base(object):
    @classmethod
    def setup(self):
        print 'Base setup'


class Child(Base):
    @classmethod
    def setup(self):
        super(Child, self).setup()
        print 'child setup'


if __name__ == "__main__":
    Child.setup()
