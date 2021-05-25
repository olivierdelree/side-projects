"""
A simple programme used to reverse a string

Instructions:
Pig Latin - Pig Latin is a game of alterations played on the
English language game. To create the Pig Latin form of an English word the
initial consonant sound is transposed to the end of the word and an ay is
affixed (Ex.: "banana" would yield anana-bay). Read Wikipedia for more
information on rules.
"""

import sys


def piglatin(s):
    if len(s) < 2:
        return s + "ay"
    return s[1:] + "-" + s[0] + "ay"


def main(s):
    print(piglatin(s))


if __name__ == '__main__':
    s = sys.argv[1]
    main(s)
