import win32wnet

def printResource(resource, info = True, parent=True):
    print '=' * 80
    for elem in dir(resource):
        if not elem.startswith('_'):
            print getattr(resource, elem),

    if info:
        print
        print
        print 'info:'
        resinfo, path = win32wnet.WNetGetResourceInformation(resource)
        print 'path:', path
        printResource(resinfo, info=False, parent=False)
        print 'endinfo:'

    if parent:
        print
        print 'parent:'
        resinfo = win32wnet.WNetGetResourceParent(resource)
        printResource(resinfo, info=False, parent=False)
        print 'endinfo:'

    print
    print '=' * 80


def printAllNetworkDriveInfo():
    handle = win32wnet.WNetOpenEnum(3, 1, 19, None)
    resources = win32wnet.WNetEnumResource(handle)
    for r in resources: print; printResource(r)
    win32wnet.WNetCloseEnum(handle)

if __name__ == '__main__':
    printAllNetworkDriveInfo()

