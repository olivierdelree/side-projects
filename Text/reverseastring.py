"""
A simple programme used to reverse a string

Instructions:
Reverse a String - Enter a string and the program will reverse it and print it
out.
"""

import sys


def reversesimple(s):
    return s[::-1]


def reverselong(s):
    rev = []
    for char in s:
        rev.insert(0, char)
    return "".join(rev)


def main(s):
    print(reversesimple(s))
    print(reverselong(s))


if __name__ == '__main__':
    s = sys.argv[1]
    main(s)
