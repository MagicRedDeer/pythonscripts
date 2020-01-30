#!C:\python27\python.exe

import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "<b>Hello world!</b>"

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 80,
        'server.socket_host': '10.10.0.212'})
    cherrypy.quickstart(HelloWorld())
