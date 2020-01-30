#coding: utf-8
import os

fname = "ș.txt"
with open(fname, "w") as f:
    f.write("hi")

files = os.listdir(u".")
print "fname: ", fname
print "files: ", files

if fname in files:
    print "found"
else:
    print "not found"
