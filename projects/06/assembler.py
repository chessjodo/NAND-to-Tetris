#!/usr/bin/env python3
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
for key in COMP.keys():
    if matched := re.search("(\||\+|\-)", key):
        new_key = key[: matched.start()] + "\\" + key[matched.start() :]
        COMPKEYS.append(new_key)
    else:
        COMPKEYS.append(key)
LABELKEYS = []


def return_value(text):
    try:
        return f"0{int(text[1:]):015b}"
    except:
        # print("TEXT: ", text)
        if matched := re.search("({})".format("|".join(LABELKEYS)), text):
            # print("PrintLABEL DICT", LABEL_DICT, matched.groups())
            # print("RegEx Labelkeys: ", "({})".format("|".join(LABELKEYS)))
            return f"0{int(LABEL_DICT[matched.group(1)]):015b}"
        else:
            if matched := re.search("R(1[0-5]|[0-9])", text):
                return f"0{int(matched.group(1)):015b}"
            else:
                if matched := re.search(
                    "({})".format("|".join(SYMBOLS)), text
                ):
                    return f"0{int(SYMBOLS[matched.group(1)]):015b}"
                else:
                    SYMBOLS[text] = f"{len(SYMBOLS)+9}"
                    print(text + ":: New Symbol")
                    return f"0{int(SYMBOLS[text]):015b}"


def update_labelkeys():
    for key in LABEL_DICT.keys():
        new_key = ""
        for char in key:
            if matched != re.match("[^a-zA-Z0-9]", char):
                new_key += "\\" + char
            else:
                new_key += char
            # print(new_key)
        LABELKEYS.append(new_key)
    # print(LABELKEYS)


def assembler():
    """
    DOCSTRING

    """
    output = open("translation.hack", "w")
    input_file = open("input.txt", "r")
    line_count = -1
    while line := input_file.readline():
        line_count += 1
        line = line.replace(" ", "")
        # print("COMPKEYS: ", COMPKEYS)
        if matched := re.match("@[^\s^X^ ]*", line):
            # print("XXX" + line[matched.start() : matched.end()] + "XXX")
            translation = return_value(line[matched.start() : matched.end()])
            # print("TRANSLATION: ", translation)
            output.writelines(translation + "\n")
        elif matched := re.match(
            "(({})=)?({})(;({}))?XX".format(
                "|".join(DESTKEYS), "|".join(COMPKEYS), "|".join(JUMPKEYS)
            ),
            line,
        ):
            # print("GROUPS: ", line, matched.groups())
            dest = DEST[matched.group(2)]
            comp = COMP[matched.group(3)]
            jump = JUMP[matched.group(5)]
            combination = f"111{comp}{dest}{jump}"
            # print("COMBINATION ", combination)
            output.writelines(combination + "\n")
        else:
            print(
                "(({})=)?({})(;({}))?".format(
                    "|".join(DESTKEYS), "|".join(COMP), "|".join(JUMPKEYS)
                )
            )
            print("No Output: ", line, ord(line[-4]), "Char -4", line[-4])
    output.close()


def add_labels():
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
        # if matched := re.search("\s*", line):
        #   line = line[: matched.start()] + line[matched.end()]
        if matched := re.search("\((.*)\)", line):
            LABEL_DICT[matched.group(1)] = line_count
            line_count -= 1
            continue
        else:
            input_file.writelines(line + "XX\n")


if __name__ == "__main__":
    print("Running Assembler")
    add_labels()
    update_labelkeys()
    assembler()
