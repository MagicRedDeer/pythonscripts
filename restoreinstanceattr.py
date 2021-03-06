
class MyClass(object):
    myAttr = 1

    def _restoreMyAttr(attrName='myAttr'):
        def _decorator(method):
            def _wrapper(self, *args, **kwargs):
                val = getattr(self, attrName)
                ret = method(self, *args, **kwargs)
                setattr(self, attrName, val)
                return ret
            return _wrapper
        return _decorator

    @_restoreMyAttr()
    def attrChanger(self):
        self.myAttr= 7
        self.printMyAttr()

    def printMyAttr(self):
        print 'myAttr=%d'%self.myAttr

if __name__ == "__main__":
    c= MyClass()
    c.printMyAttr()
    c.attrChanger()
    c.printMyAttr()

