#!/usr/bin/env python
# Take CMP Downloaded CAV file and import the Usage date to Influx

import csv
from datetime import datetime
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import sys


token = ''
org = ""
url = ""
bucket=""


client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


def main(csv_file):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    with open(csv_file, 'r')  as f:
        reader = csv.reader(f)
        for row in reader:
            #print(row)
            # https://www.cmpco.com/smartenergy/understandyourusage/downloadusagedata
            # account,serviceporint,meterid,datetime,meterchannel,usage
            account = row[0]
            serviceporint = row[1]
            meterid = row[2]
            # 4/3/2023 12:00:00 AM
            date_time = datetime.strptime(row[3], "%m/%d/%Y %I:%M:%S %p")
            meterchaneel = row[4]
            usage = float(row[5])

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