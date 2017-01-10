#!/usr/bin/env python

"""
This script is used to turn on and off VMs on a ESXi Host.
"""

from pysphere import VIServer
from texttable import Texttable
from netmiko import ConnectHandler
import sys
import argparse
import ssl

# esxhost = 'http://10.5.6.200:8080/sdk'
esxhost = '10.5.6.200'
esxurl = 'https://'+esxhost+'/sdk'

username = 'root'
password = '1234567'

esxiserver = {
    'device_type': 'linux',
    'ip': esxhost,
    'username': username,
    'password': password,
    'verbose': False       # optional, defaults to False
}

vmindex = {}

server = VIServer()

default_context = ssl._create_default_https_context

try:
        ssl._create_default_https_context = ssl._create_unverified_context
        server.connect(esxurl, esxiserver['username'], esxiserver['password'])
finally:
    ##DO NOT DO the following line or else you'll get "ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed" error
    ##ssl._create_default_https_context = default_context
    print "vserver: AFTER CONNECTION - [{}] [{}]".format(server.get_server_type(), server.get_api_version())

def initargs():
    """ initialize variables with command-line arguments """
    parser = argparse.ArgumentParser(description='input -f [file]')
    parser.add_argument('-s', '--shutdown', \
        help='Shutdown ESX host', \
        action='store_true')
    parser.add_argument('-o', '--on', \
        help='Start Machines')

    arg = parser.parse_args()

    return arg

def poweronvm(vmpath):
    vm = server.get_vm_by_path(vmpath)
    print "Powering On: " + vm.get_property('name'),
    vm.power_on()
    print "..Done"

def poweroffvm(vmpath):
    vm = server.get_vm_by_path(vmpath)
    print "Powering Off: " + vm.get_property('name'),
    vm.power_off()
    print "..Done"

def showdownhost():

    net_connect = ConnectHandler(**esxiserver)

    output = net_connect.send_command('poweroff')
    print "\n".join(output)

    sys.exit("ESX Host shutting Down")

def getvmlist():
    vmpathlist = server.get_registered_vms()
    counter = 0

    print "Loading...",
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.add_row(['VMID','Friendly Name','Hostname','IP Address','Power State'])

    for vmpath in vmpathlist:
        counter += 1
        vm = server.get_vm_by_path(vmpath)
        # vmdetails = vm.get_properties()

        name = vm.get_property('hostname')

        vmindex[counter] = {}
        vmindex[counter]['vmid'] = counter
        vmindex[counter]['hostname'] = name

        vmindex[counter]['vmipaddress'] = vm.get_property('ip_address')
        vmindex[counter]['vmfriendlyname'] = vm.get_property('name')
        vmindex[counter]['vmfilename'] = vmpath
        vmindex[counter]['powerstate'] = vm.get_status()
        vmindex[counter]['networks'] = vm.get_property('net')
        
        print str(counter) + " ",
        table.add_row([vmindex[counter]['vmid'], \
            vmindex[counter]['vmfriendlyname'], \
            vmindex[counter]['hostname'], \
            vmindex[counter]['vmipaddress'], \
            vmindex[counter]['powerstate']])

    print "...Done!"

    print(table.draw())

options = ''

args = initargs()

if args.shutdown == True:
    showdownhost()
elif args.on:
    vmliststr = args.on
else:
    vmliststr = False


while options.lower() != 'q':
    getvmlist()


    if vmliststr:
        listofid = vmliststr.split(",")
        del vmliststr
        vmliststr = False
    else: 
        print "\nEnter VMID to toggle power for seperated by Spaces or"
        print "AON or All VMs on or AOFF for All VMS off"
        print "Press Enter to Refresh"
        print "SHUTDOWN to shutdown ESX host"
        options = raw_input("or q to quit: ")

        listofid = options.split()


    for vmid in listofid:
        try:
            vmid = int(vmid)
            if vmindex[vmid]['powerstate'] == 'POWERED OFF':
                poweronvm(vmindex[vmid]['vmfilename'])
            elif vmindex[vmid]['powerstate'] == 'POWERED ON':
                poweroffvm(vmindex[vmid]['vmfilename'])
            else:
                print "Power State Error"

        except KeyError:
            print "Invalid VMID" + str(vmid)

        except ValueError:
            if vmid.lower() == 'aon':
                for vm in vmindex:
                    if vmindex[vm]['powerstate'] == 'POWERED OFF':
                        poweronvm(vmindex[vm]['vmfilename'])
            elif vmid.lower() == 'aoff':
                for vm in vmindex:
                    if vmindex[vm]['powerstate'] == 'POWERED ON':
                        poweroffvm(vmindex[vm]['vmfilename'])
            elif vmid.lower() == 'shutdown':
                showdownhost(esxhost, username, password)
            elif vmid.lower() == 'q':
                pass
            else:
                print "Invalid option"
