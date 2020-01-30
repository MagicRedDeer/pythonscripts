import heapq
import random

names = [chr(x) for x in xrange(65, 75)]
data = []
for x in range(len(names)):
    num = random.randint(0, 50)
    data.append(( num, names[x] ))

print data
heapq.heapify(data)
print data


for x in range(len(names)):
    print heapq.heappop(data)


