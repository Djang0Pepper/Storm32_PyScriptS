import sys
import os

def myfunction(mystring):
    print(mystring)


if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])