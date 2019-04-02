#!/bin/bash
# 
# Script to start and check status of a VM in AWS EC2
#

COMMAND=$1
AWSVM_INSTANCE="i-0e48607d26696aca2"
SSHKEY="~/.ssh/KaliKey.pem"
SSHUSER="ec2-user"

## Test if needed utliities are installed
if [[ ! -e /usr/local/bin/jq ]]; then
    echo "ERROR jq not installed (json parser)"
    exit 255
fi

if [[ ! -e /usr/local/bin/aws ]]; then
    echo "ERROR aws not installed (awscli)"
    exit 255
fi

## Functions
start_awsvm() {
    echo "Starting Kali Instance"
    aws ec2 start-instances --instance-ids $AWSVM_INSTANCE > /dev/null
}

connect_awsvm() {
    AWSVM_IP=`aws ec2 describe-instances --instance-ids $AWSVM_INSTANCE | jq .Reservations[0].Instances[0].PublicIpAddress |egrep -o "([0-9]{1,3}\.){3}[0-9]{1,3}"`
    ssh -i $SSHKEY $SSHUSER@$AWSVM_IP
    exit 1
}

status_awsvm() {
    TMPFILE=`mktemp -t awsinfo`
    aws ec2 describe-instances --instance-ids $AWSVM_INSTANCE > $TMPFILE

    echo -n "System Status: "
    cat $TMPFILE | jq .Reservations[0].Instances[0].State.Name
    echo -n "Public IPs: " 
    cat $TMPFILE | jq .Reservations[0].Instances[0].PublicIpAddress

    #echo $TMPFILE
    # Remove Temp File
    rm $TMPFILE
}

display_usage() {
     echo "Options"
    echo "-------"
    echo "connect - connect via SSH to Host"
    echo "start - Start VM host"
    echo "status - Host status"
}

### Main
case $COMMAND in
    start)
        start_awsvm
        ;;
    connect)
        connect_awsvm
        ;;
    status)
        status_awsvm
        ;;
    *)
        display_usage
        ;;
esac
