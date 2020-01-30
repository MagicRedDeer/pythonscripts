
import urllib2

try:

    # Create an OpenerDirector with support for Basic HTTP Authentication...
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='PDQ Application',
            uri='https://10.10.2.124:8080', user='talha.ahmed',
            passwd='lovethywife')
    opener = urllib2.build_opener(auth_handler)
    # ...and install it globally so it can be used with urlopen.
    urllib2.install_opener(opener)
    fd = urllib2.urlopen('https://www.gmail.com')
    print fd.read()


except:
    import traceback
    traceback.print_exc()

print 'Done'
raw_input()
