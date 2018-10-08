#!/usr/bin/env python3
"""
    credit: Arsia Ardalan
    repo: https://github.com/ArsiaArdalan/python-csv-parser
"""
import sys
import keyboard
import re
import unittest
import datetime
from operator import itemgetter


# TODO: lockdown deps


def _open_file(filepath):
    """
        -args: filepath
        -returns: file stream
        Opens the file in read mode and returns a filestream
    """
    # TODO: must use sys.argv and use correct path
    # TODO: exception handling for corrupt file or wrong format
    try:
        f = open(filepath, "r")
    except FileNotFoundError as fnf:
        print(
            f'ERROR: File to parse does not exist in ./CSV directory '
            f'\nTraceback: {fnf}'
        )
    else:
        return f


def _sort_date_make_model(filepath, data):
    """
        -args: 
            filepath
            data, dictionary of lists, processed data
        -returns: sorted dictionary based on columns
        Checks to see if columns of interest are in the file
        If so, returns a sorted dictionary based on the specified columns, if not, returns the unsorted dictionary 
    """
    # check to see if three headings date, make, model exist?
    (col, headings) = _get_headings_and_colSize(filepath)
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
            print(f'\n\nResult for {filepath}')
            # Confirm that we indeed sorted
            print(
                '! Note: Data sorted based on all three columns date, make, model :')
            new_list = sorted(data, key=itemgetter(
                'entrydate', 'make', 'model'))
            return new_list
    else:
        # Confirm that we didn't have all three columns to sort
        print('! Note: data not sortable... printing as is:')
        return new_list


def _get_headings_and_colSize(filepath):
    """
        -args: filepath
        -returns: tuple 
            col_size: integer, size of columns
            headings: list of strings, column headings
        Opens the file, reads the very first line, splits on comma and returns a tuple. 
    """
    f = _open_file(filepath)
    headings = []
    if f.mode == "r":
        raw_headings = f.readline().split(',')
        for h in raw_headings:
            headings.append(h.strip())
        col_size = len(headings)
    f.close()
    return (col_size, headings)


def _find_datetime_regex(data):
    """
        -args: data, data in every cell, of type string
        -returns: boolean
        Checks to see if a data point matches the regex of format 'Nov 15 2004  9:01:00:596AM' and returns
            True if so, Flase otherwise
        # REF: datetime regex made here: https://regex101.com/
        # \s?([A-Z]\w{2})\s+?(\d+)\s+?(\d+)\s+?(\d+):(\d+):(\d+):(\d+)(AM|PM)
    """
    regex = r"\s?([A-Z]\w{2})\s+?(\d+)\s+?(\d+)\s+?(\d+):(\d+):(\d+):(\d+)(AM|PM)"
    matches = re.search(regex, data)
    if(matches):
        _convert_dates_to_datetime(matches.group())
        return True

    return False


def _print_basic_info(obj):
    """
        -args: obj: an iteratable object, in this case a dictionary
        -returns: void
        Prints some keys and values
    """
    for index, value in enumerate(obj):
        print('Row[{index}] : {year}, {make}, {model}'.format(
            make=value['make'],
            model=value['model'],
            index=index,
            year=(value['entrydate']).year)
        )


def _convert_dates_to_datetime(date):
    """
        -args: date, of type string
        -return: datetime object
        Converts a given string with the format of '%b %d %Y  %I:%M:%S:%f%p' to a datetime object
    """

    datetime_format = '%b %d %Y  %I:%M:%S:%f%p'
    formatted_date = datetime.datetime.strptime(date, datetime_format)

    return formatted_date


def read_csv(filepath):
    """
        -args: filepath
        -returns: void
        Reads the file, retrieves data based on regex:
            REF: taken and modified from: https://stackoverflow.com/questions/18144431/regex-to-split-a-csv
            (?:,|\n|^)(\"(?:(?:\"\")*[^\"]*)*\"|[^\",\n]*|(?:\n|$))
        For the number of calculated rows, adds data to a dictionary and appends to the obj list
    """

    (col_size, headings) = _get_headings_and_colSize(filepath)
    f = _open_file(filepath)
    if f.mode == "r":
        new_data = re.findall(
            "(?:,|\n|^)(\"(?:(?:\"\")*[^\"]*)*\"|[^\",\n]*|(?:\n|$))", f.read())
    f.close()

    # -1 for EOF
    row_size = int(len(new_data)/col_size) - 1

    # refraining from using 'object': python class
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

                    dic[h] = new_data[i]
                    i = i + 1
            count = count + 1
        obj.append(dic)

    # sorting the object
    obj = _sort_date_make_model(filepath, obj)

    # Printing some basic info
    _print_basic_info(obj)


def main():

    read_csv('./CSV/test.csv')
    read_csv('./CSV/test2.csv')


if __name__ == "__main__":
    main()
