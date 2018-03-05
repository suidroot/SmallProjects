#!/usr/bin/which python
# Template v1.0
#
# Author:
# Version:
#

from __future__ import print_function

__author__ = "Ben Mason"
__copyright__ = "Copyright 201x"
__version__ = "0.0.1"
__email__ = "locutus@the-collective.net"
__status__ = "Development"

def initargs():
    import argparse

    """ initialize variables with command-line arguments """
    parser = argparse.ArgumentParser(description='input -f [file]')
    parser.add_argument('-e', '--enable', \
        help='Option with input', \
        default='')
    parser.add_argument('-t', '--true', \
        help='True false', \
        action='store_true')

    arg = parser.parse_args()

    return arg

def main():
    pass


if __name__ == "__main__":
    args = initargs()
    main()
