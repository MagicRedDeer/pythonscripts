import sys
import time

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

errhandler = logging.StreamHandler(sys.stderr)
outhandler = logging.StreamHandler(sys.stdout)
errhandler.setLevel(logging.WARNING)
outhandler.setLevel(logging.INFO)

logger.addHandler(errhandler)
logger.addHandler(outhandler)

for i in range(100):
    if i % 10 == 0:
        time.sleep(1)

    logger.warning({ 'Count': i })

sys.exit()

