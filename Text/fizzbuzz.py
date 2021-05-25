"""
A simple programme playing the game FizzBuzz

Instructions:
Fizz Buzz - Write a program that prints the numbers from 1 to 100. But for
multiples of three print “Fizz” instead of the number and for the multiples
of five print “Buzz”. For numbers which are multiples of both three and five
print “FizzBuzz”.
"""

import sys


def fizzbuzz(count):
    fizz = 3
    buzz = 5
    for num in range(count + 1):
        if num % fizz == 0:
            print("Fizz")
        elif num % buzz == 0:
            print("Buzz")
        elif num % (fizz * buzz) == 0:
            print("FizzBuzz!")
        else:
            print(num)


def main(count):
    fizzbuzz(count)


if __name__ == '__main__':
    try:
        count = int(sys.argv[1])
    except ValueError:
        count = 10

    main(count)
