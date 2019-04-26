#!/bin/sh


if [ ! -x ~/.updated ]; 
    sudo apt update
    sudo apt upgrade
    sudo apt install clinfo unzip p7zip-full
    sudo apt install build-essential linux-headers-$(uname -r) # Optional
    sudo apt-get install -yq python3-pip
    sudo pip3 install psutil
    touch ~/.updated
    sudo reboot
fi 

rm ~/.updated

echo "Downloading hashcat"
wget https://hashcat.net/files/hashcat-5.1.0.7z
7z x hashcat-5.1.0.7z

echo "Downloading Work lists"
mkdir ~/wordlists
git clone https://github.com/danielmiessler/SecLists.git ~/wordlists/seclists
wget -nH http://downloads.skullsecurity.org/passwords/rockyou.txt.bz2 -O ~/wordlists/rockyou.txt.bz2
cd ~/wordlists
bunzip2 ./rockyou.txt.bz2

echo "Cleaning up Home Dir"
mkdir ARCHIVE
mv hashcat-5.1.0.7z Nvidia_Cloud_EULA.pdf README ARCHIVE/
