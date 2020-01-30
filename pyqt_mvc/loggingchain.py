import logging
import sys

class Handler(logging.Handler):
    def __init__(self):
        super(Handler, self).__init__()

    def emit(self, record):
        print 'barf:', self.format(record)

logging.basicConfig(stream=sys.stdout)

logger = logging.getLogger(__name__)
logger.addHandler(Handler())
logger.error('ha')

logger2 = logging.getLogger(__name__ + ".special")
logger2.error('test')



import testmod
