#!/usr/bin/env python3

import sys
import keyboard


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

    try:
        while True:
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                sys.exit(0)
    except BaseException as e:
        print(f'exiting...')


if __name__ == "__main__":
    main()
