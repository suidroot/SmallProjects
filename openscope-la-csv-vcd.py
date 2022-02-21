#!/usr/bin/which python3
""" OPenScope MZ CSV export to VCD format converter
#
# Author:
# Version:
#
"""

import csv
import sys
from vcd import VCDWriter

__author__ = "Ben Mason"
__copyright__ = "Copyright 2017"
__version__ = "0.0.1"
__email__ = "locutus@the-collective.net"
__status__ = "Development"

def initargs():
    import argparse

    """ initialize variables with command-line arguments """
    parser = argparse.ArgumentParser(description='input -f [file]')
    parser.add_argument('-i', '--input', \
        help='Input CSV file name', \
        default='WaveformsLiveData.csv')
    parser.add_argument('-o', '--output', \
        help='Output CSV file name', \
        default='text.vcd')
    parser.add_argument('-d', '--debug', \
        help='Turn on Debugging', \
        action='store_true')

    arg = parser.parse_args()

    return arg

def loadcsvfile(filename):

    data = []

    with open(filename, 'rU') as filehandle:
        reader = csv.DictReader(filehandle, dialect='excel', quotechar='"')
        fields = reader.fieldnames

        # figure out number of LA channels
        numofchannels = 0
        for item in reader.fieldnames:
            if 'LA' in item:
                numofchannels = numofchannels + 1

        numofchannels = int(numofchannels / 2)

        for line in reader:
            # odict_keys(['Osc Ch 1 s', 'Osc Ch 1 V', '', 'LA Ch 1 s', 'LA Ch 1 V', 'LA Ch 2 s', 'LA Ch 2 V', 'LA Ch 3 s', 'LA Ch 3 V', 'LA Ch 4 s', 'LA Ch 4 V'])
            row = []

            if DEBUG:
                print ("Line: ", line)

            for channelnum in range(1, numofchannels + 1):
                print ("Channel Num:", channelnum)
                timename = 'LA Ch ' + str(channelnum) + ' s'
                valuename = 'LA Ch ' + str(channelnum) + ' V'

                if line[timename] is not '' or None: # or line[timename] is not None:
                    if channelnum != 1:
                        row.append(int(line[valuename]))
                    else:
                        if DEBUG:
                            print ("Time Name:", timename)
                            print ("Time Val: ", line[timename])
                            print ("Data Val: ", line[valuename])
                        row.append(float(line[timename]))
                        row.append(int(line[valuename]))

                else:
                    row.append(int(0))

            if DEBUG:
                print ("Row ", row)
            data.append(row)

        return data, numofchannels

def writevcdfile(data, numofchannels, filename):

    # Sort the data based on first item (time)
    def getKey(item):
        return item[0]

    sorted(data, key=getKey)

    print (data)

    with VCDWriter(sys.stdout, timescale='1 ns', date='today') as writer:

        vcdchannel = []
        # setup channels
        for counter in range(1, numofchannels+1):
            vcdchannel.append(writer.register_var('D'+str(counter), 'counter', 'integer', size=8))

        # add channel data
        for row in data:
            print (row)
            for channel in range(1, numofchannels+1):
                writer.change(vcdchannel[channel], row[0], row[1+channel])


if __name__ == "__main__":
    args = initargs()
    DEBUG = args.debug
    data, numofchannels = loadcsvfile(args.input)
    writevcdfile(data, numofchannels, args.output)
