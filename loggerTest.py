import logging
import sys
import json

class MyHandler(logging.Handler):
    'A handler'
    def emit(self, record):
        print record.getMessage()
        print 'handler got:', self.format(record)

formatter = logging.Formatter('%(name)s:%(levelname)s:%(asctime)s: %(message)s')

basename = 'HELLO'

json_data = json.dumps({'max': 100, 'done': 50})


logging.LogRecord


logger = logging.getLogger(basename)
logger1 = logging.getLogger(basename + '.logger1')
logger2 = logging.getLogger(basename + 'logger2')

handler = MyHandler()
logger.setLevel(logging.INFO)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

try:
    raise Exception, 'just for the heck of it'
except:
    print sys.exc_info()
    logger.exception('yeah')




logger.info(json_data)
logger1.info('hello1')
logger2.info('hello2')

print 'done'
