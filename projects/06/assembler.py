#!/usr/bin/env python3
import os
import re
from sys import stdin

DEST = {
    None: "000",
    "M": "001",
    "D": "010",
    "DM": "011",
    "MD": "011",
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
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
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

DESTKEYS = [key for key in DEST.keys() if key != None]
JUMPKEYS = [key for key in JUMP.keys() if key != None]
COMPKEYS = []
# Insert escape characters if special characters are used in COMP key
for key in COMP.keys():
    if matched := re.search("(\||\+|\-)", key):
        new_key = key[: matched.start()] + "\\" + key[matched.start() :]
        COMPKEYS.append(new_key)
    else:
        COMPKEYS.append(key)
LABELKEYS = []


def return_value(text):
    """
    return_value(text): Takes a string (text) which starts with a '@' sign and
    translates it to a 16 digit binary code which is returned.
    To do this the characters after the @ are checked.
    If they are integers, the integer is returned in binary.
    If it is the name of a label elsewhere in the code,
    the line number is taken from the label dictionary.
    If it is an R0-R15 code or another predifined symbol,
    the values are also taken from the respective dictionary.
    If the symbol does not yet exist, it is defined and added to the dictionary.
    """
    try:
        return f"0{int(text[1:-2]):015b}"
    except:
        if matched := re.search("({})XX".format("|".join(LABELKEYS)), text):
            return f"0{int(LABEL_DICT[matched.group(1)]):015b}"
        else:
            if matched := re.search("R(1[0-5]|[0-9])XX", text):
                return f"0{int(matched.group(1)):015b}"
            else:
                if matched := re.search(
                    "({})XX".format("|".join(SYMBOLS)), text
                ):
                    return f"0{int(SYMBOLS[matched.group(1)]):015b}"
                else:
                    SYMBOLS[text[:-2]] = f"{len(SYMBOLS)+9}"
                    return f"0{int(SYMBOLS[text[:-2]]):015b}"


def update_labelkeys():
    """
    update_labelkeys(): Goes through the keys of the LABEL_DICT dictionary and
    adds any necessary escape characters to the keys.
    The altered keys are added to an array which is used to create
    the regular expression to look for labels.
    """
    for key in LABEL_DICT.keys():
        new_key = ""
        for char in key:
            if matched != re.match("[^a-zA-Z0-9]", char):
                new_key += "\\" + char
            else:
                new_key += char
        LABELKEYS.append(new_key)


def translate_instruction(line):
    """
    translate_instruction(line): takes a string (line) and sees if it is of
    the form    DEST=COMP;JUMP
    which is the setup of any instruction.
    The values for the respective parts are retrieved from the respective
    dictionaries and combined into a single 16-bit binary string
    that is returned.
    If the line does not match the format False is returned.
    """
    if matched := re.match(
        "(({})=)?({})(;({}))?XX".format(
            "|".join(DESTKEYS), "|".join(COMPKEYS), "|".join(JUMPKEYS)
        ),
        line,
    ):
        dest = DEST[matched.group(2)]
        comp = COMP[matched.group(3)]
        jump = JUMP[matched.group(5)]
        combination = f"111{comp}{dest}{jump}"
        return combination
    return False


def assembler():
    """
    assembler(): Function that coordinates the translation from assembly to
    binary codes. It reads an input file and writes to an output file.
    For every line in the input it matches it to a value using the return_value
    function, and if that is not successful an instruction using the
    translate_instruction function. The returned values from these functions is
    written to the output file.
    """
    output = open("translation.hack", "w")
    input_file = open("input.txt", "r")
    while line := input_file.readline():
        line = line.replace(" ", "")
        if matched := re.match("@[^\s^X^ ]*XX", line):
            translation = return_value(line[matched.start() : matched.end()])
            output.writelines(translation + "\n")
            print(translation)
        elif combination := translate_instruction(line):
            output.writelines(combination + "\n")
            print(combination)
        else:
            print("The entered text is not in the asked format")
    output.close()
    input_file.close()


def add_labels():
    """
    add_labels(): Reads input from the standarn input and
    goes through every line removing the following:
    - full line comments
    - in-line comments
    - spaces before the command
    - spaces after the command

    If the line contains a label definition of the form (<labelname>), this
    is added to the LABEL_DICT witht the line number as the value.
    These lines are then removed.
    The two characters XX are added to the end of every remaining line
    containing a command to later know where the instruction ends.
    These lines are written to the input file, so that it can be traversed more
    than once later on.
    """
    input_file = open("input.txt", "w")
    line_count = -1
    while line := stdin.readline():
        line_count += 1
        line = line[:-2]
        if line == "" or line[0:2] == "//":
            line_count -= 1
            continue
        if matched := re.match("\s*", line):
            line = line[matched.end() :]
        if matched := re.search("\s*//.*", line):
            line = line[: matched.start()]
        if matched := re.search("\((.*)\)", line):
            LABEL_DICT[matched.group(1)] = line_count
            line_count -= 1
            continue
        else:
            input_file.writelines(line + "XX\n")
    input_file.close()


def full_assembly():
    """
    full_assembly():
    First calls the add_labels to traverse the entire input
    and remove any spaces and comments to only remain with the lines that
    need to be translated to binary.

    Second the function update_labelkeys is called to make sure that labelkeys
    are available with included escape characters
    to be added to regular expressions.

    The assembler function is then called to do the translation of the input.

    Lastly the input file is deleted.
    """
    add_labels()
    update_labelkeys()
    assembler()
    os.remove("input.txt")


if __name__ == "__main__":
    full_assembly()
