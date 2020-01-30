from Queue import Queue
import logging
import sys

from threading import Thread, currentThread
from time import sleep, time
from random import randint

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def worker():
    logger = logging.getLogger(currentThread().name)
    while True:

        logger.info('Waiting ... ')
        item = q.get()
        logger.info("Starting %d ..." % item)
        for i in xrange(item):
            sleep(1)
            logger.info("Step %d done!" % i)
        logger.info("%d done" % item)
        q.task_done()


def source(num, min_work, max_work):
    for i in xrange(num):
        yield randint(min_work, max_work)


if __name__ == "__main__":

    num_worker_threads = 8000
    num_items = 32000
    min_work = 2
    max_work = 5

    t0 = time()

    q = Queue()
    for i in range(num_worker_threads):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    for item in source(num_items, min_work, max_work):
        q.put(item)

    q.join()
    t1 = time()

    logging.info("finished in %d" % (t1-t0))
