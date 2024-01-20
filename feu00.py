#!/usr/bin/env python3

# Exercise 1. Echauffement / Warm up

import argparse

def check_positive_int(value):
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise ValueError
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError("Your arguments must be positive integers.")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Process two positive ints referring to the width and length of a rectangle.')
    parser.add_argument('width', type=check_positive_int, help='the width of your rectangle.')
    parser.add_argument('length', type=check_positive_int, help='the length of your rectangle.')
    args = parser.parse_args()
    return args.width, args.length

def draw_rectangle(width, length):
    if width == 1 and length == 1:
        rectangle = ["o"]
    elif width == 1:
        rectangle = ["o"] + ["|" for _ in range(length - 2)] + ["o"]
    elif length == 1:
        rectangle = ["o" + "-" * (width - 2) + "o"]
    else:
        rectangle = ["o" + "-" * (width - 2) + "o"]
        rectangle += ["|" + " " * (width - 2) + "|" for _ in range(length - 2)]
        rectangle.append("o" + "-" * (width - 2) + "o")
    return rectangle

def main():
    # Handling errors and Parsing
    width, length = parse_arguments()

    # Resolution
    display_rectangle = draw_rectangle(width, length)
    
    # Display
    print(*display_rectangle, sep="\n")

if __name__ == "__main__":
    main()
