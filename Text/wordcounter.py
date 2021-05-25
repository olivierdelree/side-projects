"""
Usage:
    wordcounter.py <input> [-o <output>]

Analyses <input> and returns unique words and their occurrences

Options:
    -h, --help          Print this help message
    -o <output>, --output <output>
                        Output to a file
    -v, --version       Print the version of the programme
"""

from docopt import docopt
import re
import texttable


def word_counter(s, ignore_case=True):
    """
    Returns a tuple made up of:
     - A dictionary of all the words from `s` and how many times they appear
     - A tuple of the number of unique words and the total number of words
    """
    if ignore_case:
        clean_s = [x.lower() for x in re.split(r"\s|\.|,", s) if x]
    else:
        clean_s = [x for x in re.split(r"\s|\.|,", s) if x]
    all_words = [word for word in clean_s]
    words_and_counts = {word: 0 for word in set(all_words)}

    for word in all_words:
        words_and_counts[word] += 1

    return words_and_counts, (len(set(all_words)), len(all_words))


def main(*args):
    try:
        with open(args[0], "r") as text:
            word_dict, counts = word_counter(text.read())
            print(
                f"The analysis found {counts[0]} unique words from a total of "
                f"{counts[1]} ({counts[0] / counts[1] * 100}%).\n")

            sorted_dict = sorted(word_dict.items(),
                                 key=lambda kv: (kv[1], kv[0]))
            table = texttable.Texttable()
            table.header([f"Words ({counts[0]})", f"Occurrence ({counts[1]})"])
            table.set_cols_align(["c", "c"])
            for word, count in sorted_dict[::-1]:
                table.add_row([word, count])

            if args[1]:
                output_stream = open(args[1], "w")
                output_stream.write(table.draw())
                output_stream.close()
                print(f"A detailed list was printed out to '{args[1]}'")
            else:
                print("Here is a detailed list:")
                print(table.draw())
    except FileNotFoundError:
        print(f"Could not find {args[0]}")


if __name__ == '__main__':
    arguments = docopt(__doc__, version=0.1)

    if arguments["<input>"]:
        if not arguments["--output"]:
            main(arguments["<input>"])
        else:
            main(arguments["<input>"], arguments["--output"])
