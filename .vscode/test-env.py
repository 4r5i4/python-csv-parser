#!/usr/bin/env python3

import sys
import keyboard
import re
import unittest
import datetime
from operator import itemgetter
# ^(\d+|\w+),([A-Z]\w{2}).*(AM|PM)
# ^(\d+)(.*)^[,]$


# datetime regex made here: https://regex101.com/
# \s?([A-Z]\w{2})\s+?(\d+)\s+?(\d+)\s+?(\d+):(\d+):(\d+):(\d+)(AM|PM)


"""
https://stackoverflow.com/questions/18144431/regex-to-split-a-csv
(?:,|\n|^)(\"(?:(?:\"\")*[^\"]*)*\"|[^\",\n]*|(?:\n|$))
"""

"""
x-get column size
x-skip the first (size) elements
x then grab every (size) element as you go

x-BONOUS: as you go, check for datetime regex


-sorting: option 1
    -done reading
    -insert into db
    -sort
    -read back from db

-sorting: option 2:
    itemgetter

x-assignment of dict key values


"""

# TODO: lockdown deps


def _open_file():
    # TODO: must use sys.argv and use correct path
    # TODO: exception handling for corrupt file or wrong format
    f = open("./CSV/test2.csv", "r")
    return f


def _sort_date_make_model(data):
    # check to see if three headings date, make, model exist?
    (col, headings) = _get_headings_and_colSize()
    target_cols = ['entrydate', 'make', 'model']
    new_list = data
    count = 0
    # don't check anything if we don't have at least the three columns (as per requirement in the assessment: year, make, model)
    # TODO: perhaps ask team what the requirement is for lowercase and UPPERCASE sorting?
    if(col >= 3):
        for t in target_cols:
            if t in headings:
                count = count + 1
        if(count == 3):
            # Confirm that we indeed sorted
            print('! Note: Data sorted based on all three columns date, make, model :')
            new_list = sorted(data, key=itemgetter(
                'entrydate', 'make', 'model'))
            return new_list
    else:
        # Confirm that we didn't have all three columns to sort
        print('! Note: data not sortable... printing as is:')
        return new_list


# for item in new_list:
#     print(item)


def _get_headings_and_colSize():
    f = _open_file()
    headings = []
    if f.mode == "r":
        raw_headings = f.readline().split(',')
        for h in raw_headings:
            headings.append(h.strip())
        col_size = len(headings)
    f.close()
    return (col_size, headings)


def _optional_print_headings(data):
    """optional, for development"""
    print('\nHeading is', data)


def _optional_print_all_data(data):
    """optional, for development"""
    for index, value in enumerate(data):
        print('\nindex[', index+1, ']value: ', value)


def _find_datetime_regex(data):
    regex = r"\s?([A-Z]\w{2})\s+?(\d+)\s+?(\d+)\s+?(\d+):(\d+):(\d+):(\d+)(AM|PM)"
    matches = re.search(regex, data)
    if(matches):
        # print(matches.group())
        _convert_dates_to_datetime(matches.group())
        return True
        # print ("Match was found at {start}-{end}: {match}".format(start = matches.start(), end = matches.end(), match = matches.group()))
        # for groupNum in range(0, len(matches.groups())):
        #     groupNum = groupNum + 1
        #     print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = matches.start(groupNum), end = matches.end(groupNum), group = matches.group(groupNum)))
    return False


def _convert_dates_to_datetime(date):
    datetime_format = '%b %d %Y  %I:%M:%S:%f%p'
    formatted_date = datetime.datetime.strptime(date, datetime_format)
    # print(formatted_date)
    return formatted_date


def read_csv():
    (col_size, headings) = _get_headings_and_colSize()
    f = _open_file()
    if f.mode == "r":
        new_data = re.findall(
            "(?:,|\n|^)(\"(?:(?:\"\")*[^\"]*)*\"|[^\",\n]*|(?:\n|$))", f.read())
    f.close()

    # -1 for EOF
    row_size = int(len(new_data)/col_size) - 1
    obj = []

    # i = col_size in order to skip the headings
    i = col_size

    for r in range(row_size):
        count = 0
        dic = {}
        for h in headings:
            if(len(dic) != len(headings)):
                if(i < len(new_data)):

                    # flag signifying we found a string matching the regex in _find_datetime_regex()
                    found_date = _find_datetime_regex(new_data[i])

                    # ...if so, replace string in-place with datetime Obj
                    if(found_date):
                        new_data[i] = _convert_dates_to_datetime(new_data[i])
                        # print('found date match')
                    # matches = re.search(regex, new_data[i])
                        # print(matches.group())
                        # print ("Match was found at {start}-{end}: {match}".format(start = matches.start(), end = matches.end(), match = matches.group()))
                        # for groupNum in range(0, len(matches.groups())):
                        #     groupNum = groupNum + 1
                        #     print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = matches.start(groupNum), end = matches.end(groupNum), group = matches.group(groupNum)))
                    dic[h] = new_data[i]
                    i = i + 1
            count = count + 1
        obj.append(dic)
    print('___________________before ', type(obj))
    obj = _sort_date_make_model(obj)
    print('___________________after ', type(obj))

    for index, value in enumerate(obj):
        print(index+1, value)

    for o in obj:
        print(o['entrydate'])


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
