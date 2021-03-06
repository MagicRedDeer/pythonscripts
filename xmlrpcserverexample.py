import datetime
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import time

def today():
    print 'called'
    today = datetime.datetime.today()
    time.sleep(1)
    return xmlrpclib.DateTime(today)

def is_ticket_valid(tic):
    return bool(tic)


server = SimpleXMLRPCServer(("localhost", 5000))
print "Listening on port 5000..."
server.register_function(today, "today")
server.register_function(is_ticket_valid, 'is_ticket_valid')
server.serve_forever()
