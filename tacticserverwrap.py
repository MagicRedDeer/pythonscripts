import sys
sys.path.append(r'D:\talha.ahmed\workspace\pyenv_maya\tactic')

if True:
    import tactic_client_lib as tcl
    import types
    import logging

    from socket import error as socketerror
    from xmlrpclib import ProtocolError


class TacticServerMeta(type):
    '''metaclass which wrap all inherited methods with retries in case of any
    error that occured due to network conditions'''

    __retries__ = 2

    def __new__(mcls, name, bases, namespace):
        namespace['__retries__'] = mcls.__retries__
        for key, value in bases[0].__dict__.items():
            if isinstance(value, types.FunctionType):
                namespace[key] = mcls._wrap(value)
        cls = super(TacticServerMeta, mcls).__new__(
                mcls, name, bases, namespace)
        return cls

    @classmethod
    def _wrap(mcls, func):
        def _wrapper(self, *args, **kwargs):
            for i in range(self.__retries__):
                try:
                    return func(self, *args, **kwargs)
                except (socketerror, ProtocolError) as e:
                    logging.error('Swallowing a Network Error: %s' % str(e))
            return func(self, *args, **kwargs)
        _wrapper.__orig_func__ = func
        _wrapper.__doc__ = func.__doc__
        return _wrapper


class TacticServer(tcl.TacticServerStub):
    '''Tactic Server Meta will wrap all calls with retries in case of error'''
    __metaclass__ = TacticServerMeta

    def copy(self):
        new_server = TacticServer(setup=False)
        new_server.set_project(self.get_project())
        new_server.set_server(self.get_server_name())
        new_server.login = self.login
        new_server.set_ticket(self.get_ticket)
        return new_server


class TacticProjectServerMeta(TacticServerMeta):
    '''Stops TacticServerMeta from wrapping the objects again'''

    def __new__(mcls, name, bases, namespace):
        namespace['__retries__'] = mcls.__retries__
        cls = super(TacticServerMeta, mcls).__new__(
                mcls, name, bases, namespace)
        return cls


class TacticProjectServer(TacticServer):
    __metaclass__ = TacticProjectServerMeta

    def __new__(cls, obj, *args, **kwargs):
        new_obj = super(TacticProjectServer, cls).__new__(*args, **kwargs)

    def say_hello(self):
        print 'hello'


if __name__ == "__main__":
    server = TacticServer(setup=True)
    server2 = TacticProjectServer(server)
    print server2, server2.ping()
    server2.say_hello()
