#!/usr/bin/env python3
"""
    credit: Arsia Ardalan
    repo: https://github.com/ArsiaArdalan/python-csv-parser
"""
import re
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


def _sort_date_make_model(filepath, data, headings):
    """
        -args: 
            filepath, used to stamp the result for respective CSV file
            data, dictionary of lists, processed data
            headings, list of columns (headings)   
        -returns: sorted dictionary based on columns
        Checks to see if columns of interest are in the file
        If so, returns a sorted dictionary based on the specified columns, if not, returns the unsorted dictionary 
    """

    # If we wanto to sort based on year of entrydate:
    # sortable_columns = ['entrydate', 'make', 'model']
    # for d in data:
    #     d['entrydate'] = d['entrydate'].year

    result = {}
    sortable_columns = ['year', 'make', 'model']

    """ check if we have all the columns needed for sorting """
    sortFlag = all(elem in headings for elem in sortable_columns)

    print(f'\n\nResult for {filepath}')
    if(sortFlag):
        """ we can sort """
        print('DATA SORTED:')
        result = sorted(data, key=itemgetter('year', 'make', 'model'))
        return result
    else:
        """ we don't have all the columns, return the obj unsorted """
        print('DATA CANNOT BE SORTED:')
        return data


def _get_headings(filepath):
    """
        -args: filepath
        -returns:
            headings: list of strings, column headings
        Opens the file, reads the very first line, splits on comma and returns a tuple. 
    """
    f = _open_file(filepath)
    headings = []
    if f.mode == "r":
        raw_headings = f.readline().split(',')
        for h in raw_headings:
            headings.append(h.strip())
    f.close()
    return headings


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
        print('[{index}] : {year}, {make}, {model}'.format(
            make=value['make'],
            model=value['model'],
            index=index+1,
            year=(value['year']))
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

    headings = _get_headings(filepath)
    col_size = len(headings)
    f = _open_file(filepath)
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

                    dic[h] = new_data[i]
                    i = i + 1
            count = count + 1
        obj.append(dic)

    # sorting the object
    sorted_obj = _sort_date_make_model(filepath, obj, headings)

    # Printing some basic info
    _print_basic_info(sorted_obj)


def main():

    read_csv('./CSV/test.csv')
    read_csv('./CSV/test2.csv')


if __name__ == "__main__":
    main()
