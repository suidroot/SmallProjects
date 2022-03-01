#!/usr/bin/env python3
''' PE File Resource content identification and extraction of contents '''

import argparse
import pefile
import magic

__author__ = "Ben Mason"
__copyright__ = "Copyright 2022"
__version__ = "0.1.0"
__email__ = "locutus@the-collective.net"
__status__ = "Development"

EXPORT_DATA = False
IGNORE_NONE_NAMES = False
FILE_SUFFIX = '.bin'

def write_file(filename, bin_data):
    ''' Write Data to a file '''

    with open(filename, 'wb') as file_handle:
        file_handle.write(bin_data)

    return 0

def main(filename):
    ''' Main function '''

    none_name_counter = 0

    # Open PE file and read contents
    thepefile = pefile.PE(filename)
    all_data = thepefile.get_memory_mapped_image()

    print(thepefile.DIRECTORY_ENTRY_RESOURCE.struct)
    print ("-----------------------")
    print()

    for entry in thepefile.DIRECTORY_ENTRY_RESOURCE.entries:

        if entry.name is None and IGNORE_NONE_NAMES:
            print ("Skipping Directory entry named None")
            continue

        print("Directory Entry: ", entry.name)
        print(entry.struct)
        print ("")
        for item in entry.directory.entries:
            print("Resource Item: ", item.name)

            for item_dir in item.directory.entries:
                print(item_dir.data.struct)
                data_rva = item_dir.data.struct.OffsetToData
                size = item_dir.data.struct.Size

                data = all_data[data_rva:data_rva+size]
                print()
                print("Data type: " + magic.from_buffer(data[0:1024]))
                print("First 20 bytes:" , end='')
                print(data[0:20])

                if EXPORT_DATA:
                    if item.name is None:
                        filename = 'Unknown_' + str(none_name_counter) + FILE_SUFFIX
                        none_name_counter += 1
                    else:
                        filename = str(item.name) + FILE_SUFFIX

                    print("Exporting content to: " + filename)
                    write_file(filename, data)

            print ("")
        print ("-----------------------")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Filename")
    parser.add_argument("-d", "--dump", help="Dump Contents to Files",
                    action="store_true")
    parser.add_argument("-i", "--ignore", help="Ignore Sections named None",
                    action="store_true")
    args = parser.parse_args()

    if args.dump:
        EXPORT_DATA = True
    if args.ignore:
        IGNORE_NONE_NAMES = True

    main(args.file)
