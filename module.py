
k = None

def updateK(val=1):
    global k
    k = val

from module import k, updateK
print k
updateK(10)
print k
