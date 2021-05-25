"""
Created 11/03/2021 by SignyaLenthiel

Instructions:
Count Vowels - Enter a string and the program counts the number of vowels in
the text. For added complexity have it report a sum of each vowel found.
"""

import sys


def countvowels(s):
    vowels = ["a", "e", "i", "o", "u", "y"]
    count = {vowel: 0 for vowel in vowels}

    text = "".join(s)
    for char in text:
        if char in count:
            count[char] += 1

    output = [f"{vow} appeared {occ} times" for vow, occ in count.items()]
    return "\n".join(output)


def main(s):
    print(countvowels(s))


if __name__ == '__main__':
    arg1 = sys.argv[1]
    main(arg1)
