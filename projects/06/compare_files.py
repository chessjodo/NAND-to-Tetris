#!/usr/bin/env python3
import sys


def compare_files(file1, file2):
    with open(file1, "r") as file1_file:
        file1_content = file1_file.read()

    with open(file2, "r") as file2_file:
        file2_content = file2_file.read()

    if file1_content == file2_content:
        print("Match successful")
    else:
        print("Match unsuccessful")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Manual: python <name>.py <file1> <file2>")
        sys.exit(1)
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    compare_files(file1, file2)
