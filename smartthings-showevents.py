#!/usr/bin/env python
# coding=utf-8

import MySQLdb as mdb
import sys
import cgi

DEBUG = False
if DEBUG:
    import cgitb
    cgitb.enable()

# Gather CGI fields
CGIDATA = cgi.FieldStorage()

SCRIPTNAME = "smartthings-showevents.py"
MAINTITLE = "SpaceCat Castle"
DATABASEHOST = "mysql.spacecatcastle.the-collective.net"

# Database information
DBDATABASE = "spacecatcastle"
DBUSERNAME = "locutusthecollec"
DBPASSWORD = "tZ?yrBde"
EVENTTABLE = "smartthingsevents"
ACTIONTABLE = "actions"
DEVICETABLE = "devices"

if CGIDATA.has_key('returnlimit'):
    try:
        DEFAULTQTY = int(CGIDATA['returnlimit'].value)
    except ValueError:
        print "<p>invalid start, not number</p>"
        DEFAULTQTY = 30
else:
    DEFAULTQTY = 30

if CGIDATA.has_key('action'):
    try:
        actionlimit = int(CGIDATA['action'].value)
    except ValueError:
        print "<p>invalid action limit</p>"
else:
    actionlimit = False

if CGIDATA.has_key('device'):
    try:
        devicelimit = int(CGIDATA['device'].value)
    except ValueError:
        print "<p>invalid device limit</p>"
else:
    devicelimit = False


def listofdevices():
    """ Gather List of devices """
    devices = []

    try:
        db = mdb.connect(DATABASEHOST, DBUSERNAME, DBPASSWORD, DBDATABASE)
        cursor = db.cursor()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    sql = """SELECT id, display_name FROM {0} ORDER BY id""".format(DEVICETABLE)

    cursor.execute(sql)
    rowcount = cursor.rowcount
    for count in range(rowcount):
        devid, display_name = cursor.fetchone()
        devices.append((devid, display_name))

    if db:
        db.close()

    return devices

def listofactions():
    """ Gather list of Actions """
    actions = []

    try:
        db = mdb.connect(DATABASEHOST, DBUSERNAME, DBPASSWORD, DBDATABASE)
        cursor = db.cursor()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    sql = "SELECT id, action FROM {0} ORDER BY id".format(ACTIONTABLE)

    cursor.execute(sql)
    rowcount = cursor.rowcount
    for count in range(rowcount):
        devid, action = cursor.fetchone()
        actions.append((devid, action))

    if db:
        db.close()

    return actions

def printevents(start=0, returnlimit=DEFAULTQTY):
    """ Query and Print List of messages """

    # Connect to Database
    try:
        db = mdb.connect(DATABASEHOST, DBUSERNAME, DBPASSWORD, DBDATABASE)
        cursor = db.cursor()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    ### Assemble Querty string
    devicequery = 'INNER JOIN {1} ON {0}.display_name = \
    {1}.id'.format(EVENTTABLE, DEVICETABLE)
    if devicelimit:
        devicequery = devicequery + ' AND {1}.id = \
        {0}'.format(devicelimit, DEVICETABLE)

    actionquery = 'INNER JOIN {1} ON {0}.name = \
    {1}.id'.format(EVENTTABLE, ACTIONTABLE)
    if actionlimit:
        actionquery = actionquery + ' AND {1}.id = \
        {0}'.format(actionlimit, ACTIONTABLE)

    sql = """SELECT {0}.description, {2}.display_name, {0}.created, {1}.action
    FROM {0}
    {3}
    {4}
    ORDER BY  `{0}`.`id` DESC
    LIMIT {5} , {6}""".format(EVENTTABLE, ACTIONTABLE, DEVICETABLE, \
        devicequery, actionquery, start, returnlimit)

    if DEBUG:
        print "<pre>{0}</pre>".format(sql)

    # run query
    cursor.execute(sql)
    rowcount = cursor.rowcount
    count = 0
    url = ""

    devices = listofdevices()
    print '<p><form action="{0}" method="get">'.format(SCRIPTNAME)
    print 'Filter on Device: <select name="device">'
    if devicelimit:
        print '<option value=""></option>'
    else:
        print '<option value="" selected></option>'

    for devid, display_name in devices:
        if devicelimit == devid:
            print '<option value="{0}" selected>{1}</option>'.format(devid, \
                display_name)
            url = url + "device={0};".format(devicelimit)
        else:
            print '<option value="{0}">{1}</option>'.format(devid, display_name)

    print "</select>"

    actions = listofactions()
    print 'Filter on Action: <select name="action">'
    if actionlimit:
        print '<option value=""></option>'
    else:
        print '<option value="" selected></option>'
    for devid, action_name in actions:
        if actionlimit == devid:
            print '<option value="{0}" selected>{1}</option>'.format(devid, \
                action_name)
            url = url + "action={0};".format(actionlimit)
        else:
            print '<option value="{0}">{1}</option>'.format(devid, action_name)

    print "</select>"

    print 'Qty Return:<input type="text" size="3" \
    name="returnlimit" value="{0}">'.format(DEFAULTQTY)
    print '<input type="submit" value="Submit"><a \
    href={0}>Reset</a>'.format(SCRIPTNAME)
    print "</form></p>"

    print """
    <table border="1">
    <tr><td>Description</td><td>Device Name</td><td>Created</td><td>Action</td></tr>
    """
    while count < rowcount:
        results = []
        results = cursor.fetchone()
        print "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>\
        </tr>".format(results[0], results[1], results[2], results[3])
        count += 1
    print "</table>"

    url = url + "returnlimit={0};".format(returnlimit)

    if int(start) == 0:
        print '<p><a href=?{2}nextevents={0}>show next {1} events</a>\
        </p>'.format(start+returnlimit+1, returnlimit, url)
    else:
        print '<p><a href=?{3}nextevents={0}>show previous {2} events</a> | \
        <a href=?{3}nextevents={1}>show next {2} events</a>\
        </p>'.format(start-returnlimit-1, start+returnlimit+1, returnlimit, url)

    if db:
        db.close()

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
    <H1>{0}</H1>""".format(MAINTITLE, title)

def printhtmlfooter():
    """ Print Started HTML Footer """
    print "</body></html>"


if __name__ == '__main__':

    printhtmlheader("SmartThings Events")

    # Clean up argument input, remove all white space and invalid characters.
    if CGIDATA.has_key('nextevents'):
        try:
            printevents(start=int(CGIDATA['nextevents'].value))
        except ValueError:
            print "<p>invalid start, not number</p>"
    else:
        printevents()

    printhtmlfooter()
