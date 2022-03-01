#!/usr/bin/which python3

import pefile
import sys
import magic
import argparse

EXPORT_DATA = False
IGNORE_NONE_NAMES = False
FILE_SUFFIX = '.bin'

def write_file(filename, bin_data):
    file_handle = open(filename, 'wb')
    file_handle.write(bin_data)
    file_handle.close()

def main(filename):

    none_name_counter = 0

    pe = pefile.PE(filename)

    all_data = pe.get_memory_mapped_image()

    print(pe.DIRECTORY_ENTRY_RESOURCE.struct)
    print ("-----------------------")
    print()

    for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:

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
                # entry.directory.entries[0].directory.entries[0].data.struct
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