
def rrange(m, values=None):
    if values is None:
        values = []
    values.append(m)
    if m > 1:
        rrange(m-1, values)
    return values

if __name__ == '__main__':
    print rrange(10)
    print rrange(11)
