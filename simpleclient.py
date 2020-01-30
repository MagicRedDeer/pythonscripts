import xmlrpclib

proxy = xmlrpclib.Server('http://localhost:5000')
print proxy.is_ticket_valid('hello')
