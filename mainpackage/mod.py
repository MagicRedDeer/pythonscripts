def main():
    print 'main:', __file__

def imported():
    print 'imported:', __file__

if __name__ == "__main__":
    main()
else:
    imported()
