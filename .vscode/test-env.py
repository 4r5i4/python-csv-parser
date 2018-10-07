#!/usr/bin/env python3

import sys
import keyboard
import re
import unittest
# ^(\d+|\w+),([A-Z]\w{2}).*(AM|PM)
# ^(\d+)(.*)^[,]$


"""
https://stackoverflow.com/questions/18144431/regex-to-split-a-csv
(?:,|\n|^)(\"(?:(?:\"\")*[^\"]*)*\"|[^\",\n]*|(?:\n|$))
"""

"""
-get column size
-skip the first (size) elements
then grab every (size) element as you go

BONOUS: as you go, check for datetime regex

-insert into db
-assignment of dict key values


"""


def _open_file():
    # TODO: must use sys.argv and use correct path
    # TODO: exception handling for corrupt file or wrong format
    f = open("./CSV/test2.csv", "r")
    return f


def _get_heading_and_colSize():
    f = _open_file()
    if f.mode == "r":
        heading = f.readline().split(',')
        col_size = len(heading)
    f.close()
    return (col_size, heading)


def _optional_print_headings(data):
    """optional, for development"""
    print('\nHeading is', data)


def _optional_print_all_data(data):
    """optional, for development"""
    for index, value in enumerate(data):
        print('\nindex[', index+1, ']value: ', value)


def read_csv():

    (col_size, headings) = _get_heading_and_colSize()
    f = _open_file()
    if f.mode == "r":
        new_data = re.findall(
            "(?:,|\n|^)(\"(?:(?:\"\")*[^\"]*)*\"|[^\",\n]*|(?:\n|$))", f.read())
    f.close()

    row_size = int(len(new_data)/col_size)
    obj = []
    i = col_size

    for r in range(row_size-1):
        count = 0
        dic = {}
        for h in headings:
            if(len(dic) != len(headings)):
                if(i < len(new_data)):
                    dic[h] = new_data[i]
                    i = i + 1
            count = count + 1
        obj.append(dic)

    for index, value in enumerate(obj):
        print(index+1, value)


def runtime_arg_check(arg_length):
    ''' takes number of arguments from command line and checks
        to see if it is exactly 2'''
    print('length of args is %d' % (arg_length))

    if arg_length < 2 | arg_length > 2:
        # raising custom exception
        raise TypeError(
            f'expected excatly 2 arguments, got {arg_length} args instead!'
            f'\n\tTry: >python parser.py <filename>.csv'
        )


def main():
    # check for correct number of args
    try:
        runtime_arg_check(len(sys.argv))
    except TypeError as e:
        print(f'Range error: {e}')

    read_csv()
    # try:
    #     while True:
    #         if keyboard.is_pressed('Esc'):
    #             print("\nyou pressed Esc, so exiting...")
    #             sys.exit(0)
    # except BaseException as e:
    #     print(f'exiting...')


if __name__ == "__main__":
    main()
