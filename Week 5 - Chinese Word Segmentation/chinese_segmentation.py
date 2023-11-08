"""
USE: python <PROGNAME> (options) WORDLIST-FILE INPUT-FILE OUTPUT-FILE
OPTIONS:
    -h : print this help message and exit
"""

import sys

MAXWORDLEN = 5


def print_help():
    """
    Generates a function string given the function name, arguments, and body.

    Args:
        name (str): The name of the function.
        args (list): A list of strings representing the function arguments.
        body (str): The body of the function.

    Returns:
        str: A string representing the function.
    """
    progname = sys.argv[0]
    progname = progname.split("/")[-1]  # strip out extended path
    help = __doc__.replace("<PROGNAME>", progname, 1)
    print("-" * 60, help, "-" * 60, file=sys.stderr)
    sys.exit(0)


if "-h" in sys.argv or len(sys.argv) != 4:
    print_help()

word_list_file = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]


def read_word_list():
    """
    Reads a word list file and returns a set of words.

    :return: A set of words read from the file.
    :rtype: set
    """
    wordset = set()
    with open(word_list_file, "r", encoding="utf-8") as f:
        for line in f:
            wordset.add(line.strip())
    return wordset


def segment(sent, wordset):
    """
    Segments a Chinese sentence into words based on a given wordset.

    Args:
        sent (str): The Chinese sentence to segment.
        wordset (set): A set of Chinese words to use as a reference for segmentation.

    Returns:
        str: The segmented sentence, with words separated by spaces.
    """

    sentence_length = len(sent)
    start_pointer, end_pointer = 0, min(sentence_length, MAXWORDLEN)
    word_list = []

    while end_pointer >= start_pointer:
        word = sent[start_pointer:end_pointer]
        if word in wordset:
            word_list.extend([word, " "])
            start_pointer = end_pointer
            end_pointer = min(start_pointer + MAXWORDLEN, sentence_length)
        else:
            end_pointer -= 1

    return "".join(word_list).strip()


def main():
    """
    Reads in an input file containing Chinese text, segments each line into individual words
    using a pre-defined word list, and writes the segmented output to an output file.
    """
    wordset = read_word_list()
    with open(input_file, "r", encoding="utf-8") as f:
        with open(output_file, "w", encoding="utf-8") as g:
            for line in f.read().split():
                print(f" {segment(line, wordset)}", file=g)


main()
