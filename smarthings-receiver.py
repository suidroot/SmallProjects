#!/usr/bin/env python
# coding=utf-8

import json
import sys
# import requests
# import time
# import cgi

DEBUG = True

if DEBUG:
    import cgitb
    cgitb.enable()


maintitle = ""
databasehost = "mysql.spacecatcastle.the-collective.net"
dbdatabase = "spacecatcastle"
dbusername = "locutusthecollec"
dbpassword = "tZ?yrBde"
dbtable = "smartthingsevents"

logfile = "st-events.log"

def createsqlstatement(data):

    datadate = data['date'].split("T")[0]
    datatime = data['date'].split("T")[1].split(".")[0]
    date = datadate + " " + datatime

    if data['physical'] == True:
        data['physical'] = 1
    else:
        data['physical'] = 0

    if data['state_changed'] == True:
        data['state_changed'] = 1
    else:
        data['state_changed'] = 0

    # sql = "INSERT INTO {0} (deviceid, stdate, value, name, \
    #         display_name, description, source, state_changed, physical, \
    #         location_id, hub_id) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}',\
    #         '{7}','{8}','{9}','{10}','{11}')".format(dbtable, \
    #          '', date, data['value'], data['name'], \
    #          data['display_name'], data['description'], data['source'], \
    #          data['state_changed'], data['physical'], '', \
    #          '')
    sql = "INSERT INTO {0} (stdate, value, name, \
            display_name, description, source, state_changed, physical) \
            VALUES ('{1}','{2}','{3}','{4}','{5}','{6}',\
            '{7}','{8}')".format(dbtable, date, data['value'], data['name'], \
             data['display_name'], data['description'], data['source'], \
             data['state_changed'], data['physical'])

    return sql


def runsql(data):
    import MySQLdb as mdb

    try:
        db = mdb.connect(databasehost, dbusername, dbpassword, dbdatabase);
        cursor = db.cursor()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)


    # sql = """CREATE TABLE devices (
    #     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #     display_name VARCHAR(60),
    #     device_id VARCHAR(40),
    #     location_id VARCHAR(40),
    #     hub_id VARCHAR(40)
    #     )"""

    sql = "SELECT id from devices WHERE device_id = '{0}'".format(data['id'])
    cursor.execute(sql)
    results = cursor.rowcount
    if results == 0:
        # print 'here'
        sql = "INSERT INTO devices values (null, '{0}', '{1}', '{2}', \
            '{3}')".format(data['display_name'], data['id'], \
            data['location_id'], data['hub_id'])
        cursor.execute(sql)
        # print sql
        deviceid = cursor.lastrowid

    else:
        deviceid = cursor.fetchone()

    data['display_name'] = int(deviceid[0])
    # print deviceid

    # name (action)
    # sql = """CREATE TABLE actions (
    #     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #     action VARCHAR(40),
    #     )"""
    sql = "SELECT id from actions WHERE action = '{0}'".format(data['name'])
    cursor.execute(sql)
    results = cursor.rowcount
    if results == 0:
        sql = "INSERT INTO actions values (null, '{0}')".format(data['name'])
        # print sql
        cursor.execute(sql)
        actionid = cursor.lastrowid
    else:
        actionid = cursor.fetchone()

    data['name'] = int(actionid[0])


    # find device info
    sql = createsqlstatement(data)


    # Execute the SQL command
    try:
        cursor.execute(sql)
        cursor.lastrowid
        db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()

    if db:
        db.close()

def createnewtable(): 

    sql = """CREATE TABLE smartthingsevents (
         
        stdate DATETIME, 
        value VARCHAR(20),
        name VARCHAR(40),
        display_name VARCHAR(60),
        description VARCHAR(20),
        source VARCHAR(20),
        state_changed BOOL,
        physical BOOL,
        location_id VARCHAR(40), 
        hub_id VARCHAR(40), 
        smartapp_id VARCHAR(40),
        created TIMESTAMP DEFAULT NOW(),
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY)"""
    
    # display_name
    # device_id
    sql = """CREATE TABLE device (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        deviceid VARCHAR(40),
        display_name VARCHAR(60),
        hub_id VARCHAR(40),
        location_id VARCHAR(40) 
        )"""

    return sql

def printhtmlheader(title):
    """ Print Standard HTML Header """

    print "Content-Type: text/html"
    print
    print """
    <html>
    <head>
    <TITLE>{0}: {1}</TITLE>
    <!-- <link rel="stylesheet" href="/style.css" /> -->
    </head>
    <body>
    <!-- <img src="/logicalis-logo.png"> -->
    <H1>{0}</H1>""".format(maintitle, title)

def printhtmlfooter():
    """ Print Started HTML Footer """
    print "</body></html>"


if __name__ == '__main__':

    # form = cgi.FieldStorage()
    try:

        # {
        # "id":"f7f20778-002b-4b2a-b606-cb8bebc66fa2",
        # "date":"2014-12-09T01:01:41.718Z",
        # "value":"40",
        # "name":"temperature",
        # "display_name":"Front Door",
        # "description":"Front Door was 40?F",
        # "source":"DEVICE",
        # "state_changed":true,
        # "physical":false,
        # "location_id":"dee85669-f468-470a-8a03-ee40910a0fa3",
        # "hub_id":"a59a88de-1681-430d-9653-76a7a8db4b84"
        # }
        data = json.load(sys.stdin)
        runsql(data)

        result = {'success':'true','message':'The Command Completed Successfully'};
        print 'Content-Type: application/json\n\n'
        print json.dumps(result)

    except:
        data = {u'id': u'56ffa847-03ad-4fa5-ac05-764c38076d06',
        u'date': u'2014-12-10T00:35:38.857Z',
        u'value': u'active',
        u'name': u'test',
        u'display_name': u'test',
        u'description': u'TEST TEST TEST',
        u'source': u'DEVICE',
        u'state_changed': True, 
        u'physical': False, 
        u'location_id': u'dee85669-f468-470a-8a03-ee40910a0fa3',  
        u'hub_id': u'a59a88de-1681-430d-9653-76a7a8db4b84'
        }

        if DEBUG:
            printhtmlheader("test")

            runsql(data)

            print data

            printhtmlfooter()
        else:
            printhtmlheader("No body home")
            printhtmlfooter()


    if DEBUG:
        f = open(logfile, 'a')
        f.write("-------\n")
        f.write(str(data) + "\n")
        f.close()

