

def afunc(l):

    try:
        l.append('some_value')
        print l
        return len(l)
    finally:
        l.remove('some_value')


if __name__ == "__main__":
    l = range(10)
    print afunc(l)

    print l


