import mainpackage

def pwd():
    import os
    print os.path.abspath(os.curdir)

def imported():
    print 'imported:', __file__

def main():
    print 'main:', __file__

if __name__ == "__main__":
    main()
else:
    imported()
pwd()
