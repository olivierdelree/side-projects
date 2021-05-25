"""
==================================================
Fibonacci Sequence Generator
==================================================
Returns a Fibonacci sequence up to the number provided or containing the amount
of numbers requested.
"""

import argparse
import sys


def main(num, upto):
    output = []
    previous_number = 1
    current_number = 1
    if upto:
        if num == 0:
            output = [0]
        elif num == 1:
            output = [1]
        else:
            output.extend([previous_number, current_number])
            addition = previous_number + current_number
            while addition <= num:
                previous_number = current_number
                current_number = addition
                output.append(current_number)
                addition = previous_number + current_number
            output.append(f"[{addition}]")
    else:
        if num == 0:
            output = [0]
        elif num == 1:
            output = [1]
        else:
            output.extend([previous_number, current_number])
            count = 2
            while count <= num:
                addition = previous_number + current_number
                previous_number = current_number
                current_number = addition
                output.append(current_number)
                count += 1

    return "\n".join(map(str, output))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="fibonacci.py",
                                     usage="%(prog)s NUMBER [--upto]")
    parser.add_argument("number",
                        type=int,
                        action="store",
                        help="Number for the sequence")
    parser.add_argument("--upto",
                        dest="upto",
                        action="store_true",
                        help="Returns a sequence up to the number provided "
                             "instead of containing n numbers "
                             "(also provides the next one in [])",
                        required=False)
    args = parser.parse_args()
    print(main(args.number, args.upto))
