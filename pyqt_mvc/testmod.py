import logging


class Handler(logging.Handler):
    def __init__(self):
        super(Handler, self).__init__()

    def emit(self, record):
        print record
        print 'barf2:', self.format(record)

logger = logging.getLogger(__name__)
logger.addHandler(Handler())
logger.error('asdf')
