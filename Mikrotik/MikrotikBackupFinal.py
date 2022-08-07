import socket, os
from ssh2.session import Session
from paramiko import SSHClient
import paramiko
from scp import SCPClient
import re, time

# Before run this script, please install bellow modules. If you have please avoid this.
# pip install scp
# pip install paramiko
# pip install ssh2-python3
# pip install ssh2-python

# ***** IMPT : Before run this script in your production enverionment, please understand the risk. You can run this script in your LAB first.


# It will remove the backup file from Mikrotik
# IMPT: If you have more than one backup file, then it will remove all.
def remove(host, user, password):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((host, 22))
    session = Session()
    session.handshake(soc)
    session.userauth_password(user, password)

    # Create Session
    channel = session.open_session()
    channel2 = session.open_session()

    output = channel.execute(f"/file print")

    size, data = channel.read()
    file_name = data.decode()

    if ".backup" in file_name:
        backup_name = re.findall(r"[0-9a-zA-Z_.-]*\.backup", file_name)

        for backups in backup_name:
            backupsx = session.open_session()
            print(f"Removing the backup ---> {backups}")
            backupsx.execute(f"/file remove [find name={backups}]")
            backupsx.close()
            print("Remove Success!!!!!")


# It will download the backup file from Mikrotik
def download(host, user, password, backup_name):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=host,
        username=user,
        password=password,
        allow_agent=False,
        look_for_keys=False,
        port=22,
    )
    scp = SCPClient(ssh.get_transport())
    scp.get(f"{backup_name}")
    scp.close()


# It will create the backup file on Mikortik
def con(ip1):

    address = ip1
    user = "admin"
    password = "123456"

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((address, 22))

    session = Session()
    session.handshake(soc)
    session.userauth_password(user, password)

    # Create Session
    channel = session.open_session()
    channel2 = session.open_session()
    channel3 = session.open_session()

    output = channel.execute(f"/file print")
    size, data = channel.read()
    file_name = data.decode()

    if ".backup" in file_name:

        print("-" * 20, "Backup file is exist", "-" * 20)
        backup_name = re.findall(r"[0-9a-zA-Z._-]*\.backup", file_name)
        # backup_name = re.findall(r"[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\.backup", file_name)
        print("-" * 20, backup_name, "-" * 20)

        if address in os.listdir():
            print("-" * 20, "Directory is exist", "-" * 20)
            os.chdir(address)

            for backup_name_new in backup_name:
                download(address, user, password, backup_name_new)
                print("*" * 20, "Backup Download success", "*" * 20, "\n")
            os.chdir("..")
        else:
            os.mkdir(address)
            os.chdir(address)

            for backup_name_new in backup_name:
                download(address, user, password, backup_name_new)
                print("*" * 20, "Backup Download success", "*" * 20, "\n")

            os.chdir("..")
    else:
        channel2.execute(f"/system backup save name={address}")
        print("-" * 20, "Backup create Success", "-" * 20)
        backupName = f"{address}.backup"

        if address in os.listdir():
            print("-" * 20, "Directory is exist", "-" * 20)
            os.chdir(address)
            download(address, user, password, backupName)
            print("*" * 20, "Backup Download success", "*" * 20, "\n")
            os.chdir("..")

        else:
            os.mkdir(address)
            os.chdir(address)
            download(address, user, password, backupName)
            print("*" * 20, "Backup Download success", "*" * 20, "\n")
            os.chdir("..")

    channel.close()
    channel2.close()


# Passing IP address
ips = open("ip_list.txt", "r")
for ip in ips:
    ip1 = ip.strip()
    print("\n", "=" * 30, f"Working on {ip1}", "=" * 30)
    con(ip1)
    time.sleep(2)
    remove(ip1, "admin", "123456")
