#!/usr/bin/which python

import csv
import subprocess

OFCSV = "/Users/locutus/Desktop/OmniFocus.csv"


with open(OFCSV, 'rU') as filehandle:
    reader = csv.reader(filehandle, dialect='excel', quotechar='"')
    for line in reader:
        if line[1] == 'Action':
            project = line[4]
            task = line[2]
            context = '+@'+line[5].replace(" ", "")
            startdate = line[6]
            duedate = line[7]
            duration = line[9]
            note = line[11]

# Built-in attributes are:
#   description:    Task description text
#   status:         Status of task - pending, completed, deleted, waiting
#   project:        Project name
#   priority:       Priority
#   due:            Due date
#   recur:          Recurrence frequency
#   until:          Expiration date of a task
#   limit:          Desired number of rows in report, or 'page'
#   wait:           Date until task becomes pending
#   entry:          Date task was created
#   end:            Date task was completed/deleted
#   start:          Date task was started
#   scheduled:      Date task is scheduled to start
#   modified:       Date task was last modified
#   depends:        Other tasks that this task depends upon

            command = ["task", "add", '"' + task + '"', "project:"+project, context]

            if duedate != '':
                command.append("due:"+duedate)
            if startdate != '':
                command.append("scheduled:"+startdate)

            subprocess.call(command)

# Task ID,Type,Name,Status,Project,Context,Start Date,Due Date,Completion Date,Duration,Flagged,Notes
# 1,Project,Miscellaneous,active,,,,,,,0,
# 1.1,Action,Check on finances,,Miscellaneous,Scheduled,2017-06-12 12:00:00 +0000,,,,0,
