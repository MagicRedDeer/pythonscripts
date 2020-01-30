import sys


class List (list):

    default = range(10)

    def __init__(self): self.ripe = False

    def __getitem__(self, integer):
        if not self.ripe:
            self.extend(List.default)
            self.ripe = True
        return super(List, self).__getitem__(integer)

    def __iter__(self):
        if not self.ripe:
            self.extend(List.default)
            self.ripe = True
        return super(List, self).__iter__()

    def __str__(self):
        return super(List, self).__str__()

    def __getslice__(self, *args, **kwargs):
        self.ripen()
        return super(List, self).__getslice__(*args, **kwargs)


    def __reversed__(self, *args, **kwargs):
        self.ripen()
        return super(List, self).__reversed__()

    def reverse(self):
        self.ripen()
        return super(List, self).reverse()

    def unripe(self):
        self.ripe = False

    def ripen(self):
        if not self.ripe:
            self.extend(List.default)
            self.ripe = True


if __name__ == "__main__":
    l = List()
    l.append(10)
    l.ripen()
    print l

