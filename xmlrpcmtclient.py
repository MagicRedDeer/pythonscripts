import xmlrpclib
import threading
import sys

import tactic_client_lib

stub = tactic_client_lib.TacticServerStub(server='dbserver',
        project='captain_khalfan', login='talha.ahmed', password='lovethywife')

def ping():
    newstub = tactic_client_lib.TacticServerStub(setup=False)
    newstub.set_server(stub.get_server_name())
    newstub.set_project(stub.get_project())
    newstub.set_ticket(stub.get_login_ticket())
    return newstub.query('vfx/asset')



#def fetch_users():
    #proxy = xmlrpclib.Server("http://dbserver:80/", allow_none=True)
    #xmlrpclib.Transport.user_agent = 'xmlrpclib.py (Windows)'
    ##proxy.set_language('python')
    #print proxy.ping(ticket)
    ##print len(proxy.get_column_info('sthpw/user'))


#fetch_users()
#sys.exit(0)

ticket ='cc3f5f342cf07fbaf6bf0f94ba6ca699' 
ticket = {
    'ticket': stub.get_login_ticket(),
    'project': stub.get_project(),
    'language': 'python'
}
def ping_simple():
    proxy = xmlrpclib.Server("http://dbserver:80/", allow_none=True)
    xmlrpclib.Transport.user_agent = 'xmlrpclib.py (Windows)'
    print proxy.ping(ticket)

def simple_test():
    ping_simple()


def thread_test():
    threads = []
    for _ in range(100):
        t = threading.Thread(target=ping, args=())
        threads.append(t)
        t.start()

    # wait for all threads to exit
    for th in threads:
        print th.join()

if __name__ == '__main__':
    simple_test()

