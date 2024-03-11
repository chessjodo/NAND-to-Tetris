#!/usr/bin/env python3
import re
from sys import stdin

DEST = {
    None: "000",
    "M": "001",
    "D": "010",
    "DM": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "ADM": "111",
}
JUMP = {
    None: "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}
COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "10110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101",
}

SYMBOLS = {
    "SCREEN": "16384",
    "KBD": "24576",
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4",
}

LABEL_DICT = {}


def return_value(text):
    try:
        return f"0{int(text[1:]):015b}"
    except:
        try:
            return f"0{int(LABEL_DICT[text[1:]]):015b}"
        except:
            if re.match("R([0-1]?[0-9])", text):
                return f"0{int(text[1:]):015b}"
            else:
                try:
                    return f"0{int(SYMBOLS[text[1:]]):015b}"
                except:
                    return "Symbol not Found"


def assembler():
    output = open("translation.hack", "w")
    line_count = -1
    while line := stdin.readline():
        line_count += 1
        line = line[:-2]
        if line == "" or line[0:2] == "//":
            continue
        elif matched := re.match("\((.*)\)", line):
            LABEL_DICT[matched.group(1)] = line_count + 1
            line_count -= 1
            continue
        if matched := re.match("@.{1,3}", line):
            translation = return_value(line)
            print(translation)
            output.writelines(translation + "\n")
        elif matched := re.match("(.*)=(.*)(;(.*))?", line):
            dest = DEST[matched.group(1)]
            comp = COMP[matched.group(2)]
            jump = JUMP[matched.group(4)]
            combination = f"111{comp}{dest}{jump}"
            print(combination)
            output.writelines(combination + "\n")
        else:
            print(line)
    output.close()


if __name__ == "__main__":
    print("Running Assembler")
    assembler()
