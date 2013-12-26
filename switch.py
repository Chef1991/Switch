#!/usr/local/bin/python


#	   _____         _ __       __
#	  / ___/      __(_) /______/ /_
#	  \__ \ | /| / / / __/ ___/ __ \
#	 ___/ / |/ |/ / / /_/ /__/ / / /
#	/____/|__/|__/_/\__/\___/_/ /_/



from __future__ import print_function
import os
import json

from termcolor import colored

nameKey = "name"
userKey = "user"
hostKey = "host"
portKey = "port"
sshKeyKey = "key"
json_file = "ssh_data.json"
def add_connection(data_dict):
    print("What would you like to name this connection?")
    name = raw_input()
    print("What is the username?")
    user = raw_input()
    print("What is the host?")
    host = raw_input()
    port = ""
    sshKey = ""
    while (port == "" or sshKey == ""):
        print("What else would you like to add?")
        print("[1] SSH key")
        print("[2] Port")
        print("[0] Nothing Else")
        input = raw_input()
        if (int(input) == 0):
            break
        elif (int(input) == 1):
            print("Enter the path to the ssh key.")
            sshKey = raw_input()
        elif (int(input) == 2):
            print("Enter the port.")
            port = raw_input()
    new_con = {nameKey: name, userKey: user, hostKey: host}
    if (port != ""):
        new_con[portKey] = port
    if (sshKey != ""):
        new_con[sshKey] = sshKey
    data_dict.append(new_con)
    with open(json_file, "w") as outfile:
        json.dump(data_dict, outfile, indent=4)


def remove_connection(data):
    print("Select which connection you would like to remove.")
    for i, d in enumerate(data):
        print("[{0}] {1}".format(i + 1, d[nameKey]))
    print("[-] Cancel")
    input = raw_input()
    if(input == '-'):
        return
    print(colored("Are you sure you want to remove the", "red"), colored(data[int(input) - 1][nameKey], "green"),
          colored("connection? (y/n)", "red"))
    res = ""
    print("y" != "y")
    while True:
        res = raw_input()
        print(res.lower())
        print(len(res))
        if res.lower() == "y" or res.lower() == "n":
            break
        else:
            print("You must enter either y or n.")

    if (res.lower() == "y"):
        data.pop(int(input) - 1)
        with open(json_file, "w") as outfile:
            json.dump(data, outfile, indent=4)


while (True):
    data = []
    home = os.path.expanduser("~")
    json_file = home + "/" + json_file
    print(json_file)
    try:
        json_data = open(json_file)
        data = json.load(json_data)
        for i, d in enumerate(data):
            print("[{0}] {1}".format(i + 1, d[nameKey]))
        print("[+] Add Connection")
        print("[-] Remove Connection")
        print("[q] quit")
    except IOError as e:
        print(colored("Could not find any saved connections", "red"))
        print("[+] Add Connection")
        print("[q] quit")
    selection = raw_input()
    if selection == 'q':
        exit()
    elif selection == '+':
        add_connection(data)
    elif selection == '-':
        remove_connection(data)
    else:
        selected = data[int(selection) - 1]

        sshStr = "ssh"
        try:
            port = selected[portKey]
            sshStr += " -p " + port
        except KeyError:
            pass
        sshStr += " " + selected[userKey] + "@" + selected[hostKey]
        try:
            sshKey = selected[sshKeyKey]
            sshStr += " -i " + sshKey
        except KeyError:
            pass
        print(colored("Connecting to {0}@{1}".format(selected[userKey], selected[hostKey]), "green"))
        os.system(sshStr)
