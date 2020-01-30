import xmlrpclib


server = xmlrpclib.ServerProxy('http://localhost:9000')
server.listdir()
