"""
Created 11/03/21 at 16:53 GMT by SignyaLenthiel

Instructions;
Check if Palindrome - Checks if the string entered by the user is a
palindrome. That is that it reads the same forwards as backwards like
“racecar”.
"""

import sys


def main(s):
    if s == s[::-1]:
        print(f"{s} is indeed a palindrome!")
    else:
        print(f"My condolences, {s} is not a palindrome...\n"
              f"Forward: {s}\n"
              f"Backward: {s[::-1]}")


if __name__ == '__main__':
    arg1 = sys.argv[1]
    main(arg1)
