# !/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# afraidUpdate.py

# import standard
import os
import sys
import subprocess
import os.path
import json
import base64

# Color for error messages
CRED = '\033[91m'
CEND = '\033[0m'

# import custom
try:
    from Crypto.Cipher import AES
except ImportError:
    installQuest = input(CRED + "Import of module \"Pycrypto\" failed." + CEND + " Install it now? (y/n) ").lower()
    if installQuest in ('y', 'yes'):
        print("Installing \"Pycrypto\" now.")
        subprocess.call("sudo -H python3.6 -m pip install pyCrypto > {}".format(os.devnull), shell=True)
        print("Installing \"Pycrypto\" successful.")
        from Crypto.Cipher import AES
    else:
        print(CRED + "Missing module. Exiting now." + CEND)
        sys.exit()

# get MAC for hashing
stdoutdataMAC = subprocess.getoutput("cat /sys/class/net/*/address | awk 'NR==1{print $1}'").upper()
stdoutdataMAC_lt = subprocess.getoutput("cat /sys/class/net/*/address | awk 'NR==2{print $1}'").upper()
if stdoutdataMAC == '00:00:00:00:00:00' and stdoutdataMAC_lt != '':
    stdoutdataMAC = stdoutdataMAC_lt

# generate key for hashing
secret_key = "{: <32}".format(stdoutdataMAC).encode("utf-8")
cipher = AES.new(secret_key,AES.MODE_ECB)

# get IPv6
stdoutdataIP6pub = subprocess.getoutput("ifconfig | grep \"inet6 \" | grep -v \"^[fe]\" | grep -v :: | awk 'NR==1{print$2}'")
stdoutdataIP6pub_lt = subprocess.getoutput("ifconfig | grep \"inet6 \" | grep -v \"^[fe]\" | grep -v :: | awk 'NR==2{print$2}'")
if stdoutdataIP6pub is "" and stdoutdataIP6pub_lt is not "":
    stdoutdataIP6pub = stdoutdataIP6pub_lt
elif stdoutdataIP6pub is "" and stdoutdataIP6pub_lt is "":
    print("It seems there is no IPv6. Exiting.")
    sys.exit()

# main function
def func():
    # check if credentials already exist
    # if not, they will be asked for
    if not os.path.exists('dyndnsUpdateCredentials.json'):
        dyndnsUrl = input("What is the DynDNS url? (something.afraid.org) ")
        dyndnsUrl = "{: <32}".format(dyndnsUrl)
        dyndnsUrl = base64.b64encode(cipher.encrypt(dyndnsUrl))
        dyndnsUrl = dyndnsUrl.decode('utf8')

        userName = input("What is your username? ")
        userName = "{: <32}".format(userName)
        userName = base64.b64encode(cipher.encrypt(userName))
        userName = userName.decode('utf8')

        userPassword = input("What is your password? ")
        userPassword = "{: <32}".format(userPassword)
        userPassword = base64.b64encode(cipher.encrypt(userPassword))
        userPassword = userPassword.decode('utf8')

        dummyDataStat = "{\"dyndnsUrl\": \"" + dyndnsUrl + "\",\"userName\": \"" + userName + "\",\"userPassword\": \"" + userPassword + "\"}"
        with open('dyndnsUpdateCredentials.json', 'w') as outfileStat:
            outfileStat.write(dummyDataStat)
    # file for credentials is found
    # trying to update
    try:
        with open('dyndnsUpdateCredentials.json') as cred_file:
            credDdns = json.load(cred_file)

            dyndnsUrl = credDdns["dyndnsUrl"]
            dyndnsUrl = cipher.decrypt(base64.b64decode(dyndnsUrl))
            dyndnsUrl = dyndnsUrl.decode('utf8').strip()

            userName = credDdns["userName"]
            userName = cipher.decrypt(base64.b64decode(userName))
            userName = userName.decode('utf8').strip()

            userPassword = credDdns["userPassword"]
            userPassword = cipher.decrypt(base64.b64decode(userPassword))
            userPassword = userPassword.decode('utf8').strip()

            updateLink = "curl https://" + userName + ":" + userPassword + "@freedns.afraid.org/nic/update?hostname=" + dyndnsUrl + "&myip=" + stdoutdataIP6pub
            subprocess.getoutput(updateLink)
    except:
        print("Something went wrong, let's try again.")

func()
