from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


import os

class OsRequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2', )

server = SimpleXMLRPCServer(("localhost", 9000),
        requestHandler=OsRequestHandler)
server.register_introspection_functions()

server.register_function(os.listdir)
server.register_function(os.chdir)
server.register_function(lambda: os.curdir, 'curdir')
server.register_function(os.path.abspath)
server.register_function(os.path.expanduser)
server.register_multicall_functions()

server.serve_forever()
