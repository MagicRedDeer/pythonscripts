from collections import OrderedDict
import cStringIO


class Attr(object):
    def __init__(self, key, default):
        self.key = key
        self.default = default

    def __get__(self, instance, owner=None):
        ':type instance: Info'
        if instance is None:
            return self
        return instance.get(self.key, self.default)

    def __set__(self, instance, value):
        ':type instance: Info'
        print 'calling set!'
        instance[self.key] = value


class Info(OrderedDict):
    def write(self):
        data = cStringIO.StringIO()
        for key, value in self.items():
            data.write('%s=%s\n' % (key, str(value)))
        return data.getvalue()


class MayaInfo(Info):
    mayaver = Attr('mayaver', '2015')
    is64 = Attr('is64', True)
    platform = Attr('platform', '')


class Maya2016Info(MayaInfo):
    mayaver = Attr('mayaver', '2016')


if __name__ == "__main__":
    i = MayaInfo(platform='win32', is64=False)
    print i.write()
    print i.mayaver
    MayaInfo.mayaver.default = '2222'
    print i.mayaver
