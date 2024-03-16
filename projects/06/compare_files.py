#!/usr/bin/env python3
import sys


def compare_files(file1, file2):
    new_file = file2.replace(".hack", ".asm")
    with open(new_file, "r") as asm_file:
        with open(file1, "r") as file1_file:
            with open(file2, "r") as file2_file:
                count = 0
                line_count = 0
                while (f1 := file1_file.readline()) and (
                    f2 := file2_file.readline()
                ):
                    asm_line = asm_file.readline()
                    line_count += 1
                    if count == 5:
                        return
                    while asm_line[0] == "(":
                        asm_line = asm_file.readline()
                    if f1 != f2:
                        print(
                            "Match unsuccessful at lines: F1: ",
                            f1,
                            " F2: ",
                            f2,
                            end="",
                        )
                        print("ASM: ", asm_line, line_count)
                        count += 1
                print("Match successful!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Manual: python <name>.py <file1> <file2>")
        sys.exit(1)
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    compare_files(file1, file2)
