#!/usr/bin/env python
# Take CMP Downloaded CAV file and import the Usage date to Influx

import csv
from datetime import datetime
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import sys
from os import getenv


token = getenv('INFLUX_TOKEN')
org = getenv('INFLUX_ORG')
url = getenv('INFLUX_URL')
bucket = getenv('INFLUX_BUCKET')


client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


def main(csv_file):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    with open(csv_file, 'r')  as f:
        
        reader = csv.DictReader(f)
        for row in reader:
            #print(row)
            # new fields (9/13/25):
            # https://resenergymanager.cmpco.com/insights
            # Name,Address,Account Number,Service,Type,Date,Start Time,End Time,Usage,Units,Costs,Weather

            # account = row['Account Number']
            # 2025-05-19 00:00:00-04:00
            # date_time = datetime.strptime(row['Start Time'], "%m/%d/%Y %I:%M:%S %p")
            date_time = datetime.strptime(row['Start Time'], "%Y-%m-%d %H:%M:%S%z")
            # meterchaneel = row[4]
            usage = float(row['Usage'])
            print(date_time, usage)
            # continue
            point = (
                Point("_measurement")
                .tag("kwh", "kwh")
                .time(date_time)
                .field("usage", usage)
            )
            write_api.write(bucket=bucket, org=org, record=point)

if __name__ == "__main__":
    if len(sys.argv) < 1:
        sys.exit()
    else:
        filename = sys.argv[1]

    main(filename)