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


def _get_heading_and_colSize():
    f = open("./CSV/test.csv", "r")
    if f.mode == "r":
        heading = f.readline().split(',')
        # _optional_print_headings()
        col_size = len(heading)
    f.close()
    return (col_size, heading)


def _optional_print_headings(data):
    print('\n\n\n\nheading is', data)


def _optional_print_all_data(data):
    for index, value in enumerate(data):
        print('\nindex[', index+1, ']value: ', value)

# def _next_data_point(index):
#     # checking for index bounds
#     result = (index < len(new_data))


def read_csv():

    (col_size, headings) = _get_heading_and_colSize()
    f = open("./CSV/test.csv", "r")
    if f.mode == "r":
        new_data = re.findall(
            "(?:,|\n|^)(\"(?:(?:\"\")*[^\"]*)*\"|[^\",\n]*|(?:\n|$))", f.read())

        # _optional_print_all_data()

        # data = (re.split('\r\n', f.read().decode('utf-8')))
        # new_data = re.findall("[^\"][^\r\n][^\"][^\r\n].*", f.read())
    f.close()
    # new_dict = {}
    # obj = []
    # d1 = {'heading: data', 'ff: 5'}
    # d2 = {'dd: 2', 'jj: 6'}
    # d3 = {'cc: 3', 'bb: 4'}
    # obj.append(d1)
    # obj.append(d2)
    # obj.append(d3)
    # print('object is ', obj)
    # for i in range(col_size):
    #     obj.append(
    #         for j in
    #     )
    # for i in range(len(new_data)):
    # for data in new_data:
    #     for i in range(10):
    #         print(data)

    # floor the num of rows
    row_size = int(len(new_data)/col_size)
    # print('row size is :', row_size)
    dic = {}
    obj = []
    i = col_size
    print(type(new_data))
    print('length of new_data is:', len(new_data))
    # for i, value in enumerate(new_data):
    #     print(i, value)

    # -1 to ignore the EOF char
    for r in range(row_size-1):
        count = 0
        dic = {}
        for h in headings:
            if(len(dic) != len(headings)):
                if(i<len(new_data)):
                    dic[h] = new_data[i]
                    i = i + 1
            count = count + 1
        # print((dic))
        obj.append(dic)

    for index, value in enumerate(obj):
        print(index+1, value)

            # print('\n\nindex:', i)
            # dic[h] = new_data[i]
            # obj.append(dic)
            # print('index[', i, ']: ', new_data[i])
            # dic[h] = new_data[i]
            # print('printing dic before appending:', dic)
        # print(obj)
    # for index, value in enumerate(obj):
    #     print(index, value)

    #         # print('row unmber ', r+1, ':', h)
    #         # dic[h] = None
    #         # dic[h] = _next_data_point(i)
    #         # i = i + 1

    # for index, value in enumerate(obj):
    #     print(index, value)

    file = open("testfile.txt", "w")
    # for i in range(10):
    #     for data in (new_data):
    #         print(data)
    #         file.write(data)
    file.close()

    # for j in range(col_size):
    #     new_dict[headings[j]] =

    # new_data = f.read().replace('"\n', '\n').replace(',\n', ',')
    # data = ((new_data).rsplit('\n'))

    # new_data = f.read().replace('\n', '*******').replace(',*******', ',')
    # new_data = f.read()
    # new_data = re.findall(
    #     "(?:,|\n|^)(\"(?:(?:\"\")*[^\"]*)*\"|[^\",\n]*|(?:\n|$))", f.read())
    # for index, value in enumerate(new_data):
    #     print('\nindex[', index+1, ']value: ', value)
    # line = re.sub('[\d]', '&', new_data)
    # print(line)
    # print(data)
    # for i in range(10):
    #     print(i)  # 0, 1, 2, ..., 9

    # get size of heading

    # dict = {}
    # for i in range(col_size):
    #     print('index', i)
    #     dict[heading[i]] = None
    # print(dict)
    # new_data = f.read().replace(',\n', '____').replace(
    #     '"\n', '*****').replace('\n', ',')
    # data = new_data.replace('*****', '\n')
    # data_er = data.split('\n')
    # for i in data_er:
    #     print('\n\n>>>>>',  i)
    # print(new_data)
    # for i in data:
    #     print('>>>>>>>___:      ', i)

    # print(lines[2])
    # rows = f.read().splitline('"\r\n')
    # heading = f.readline()
    # print('heading is ', heading)
    # line = rows[1].strip('\n\r')
    # print(line)
    # print(rows)
    # print(re.split('; |, |,, |\r\n', rows[1]))
    # print(rows[1])
    # print(rows[1])


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
