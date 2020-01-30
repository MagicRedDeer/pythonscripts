#!"c:\Program Files\Python35\python.exe"

import asyncio
import time
import selector

sleep = asyncio.sleep

@asyncio.coroutine
def slow_func(name='func1'):
    print('start', name)
    yield from sleep(1)
    print('mid', name)
    yield from sleep(1)
    print('end', name)

@asyncio.coroutine
def run_everything():
    pass

start = time.time()
loop = asyncio.get_event_loop()
asyncio.ensure_future(slow_func('func1'))
asyncio.ensure_future(slow_func('func2'))
asyncio.ensure_future(slow_func('func3'))
loop.run_forever()
end = time.time()

print('it took', end - start)

loop.close()
