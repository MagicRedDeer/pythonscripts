class Num(object):
    def __init__(self, num):
        self.num  = num
    def __eq__(self, other):
        return round(self.num) == round(other.num)

if __name__ == '__main__':
    print Num(2.6) == Num(3.4)
