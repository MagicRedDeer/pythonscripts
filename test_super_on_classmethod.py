class Base(object):
    @classmethod
    def method(self):
        return 'Base setup'


class Child(Base):
    @classmethod
    def method(self):
        return 'Child setup ' + super(Child, self).method()

def test_super_on_classmethod():
    assert Child.method() == 'Child setup Base setup'

if __name__ == "__main__":
    Child.method()

# run: nosetests test_super_on_classmethod.py
