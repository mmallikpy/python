"""
This script for cisco device backup using running config. It's get the device ip address from a file [DeviceIPList.txt].
My case my all device have multiple user and password sor I use exception.
"""

from netmiko import ConnectHandler
import os
import time

# Create a folder using Year Month Day Hour Minutes.
folder_name = time.strftime("%Y-%m-%d_%H_%M" + "_Network_device_Backup")
os.mkdir(folder_name)

# Open a text file. It's for the device IP address.
with open("DeviceIPList.txt", "r") as a_file:
    for line in a_file:
        ip_addr = line.strip()
        try:
            cisco_devices = {
                "device_type": "cisco_ios",
                "host": ip_addr,
                "username": "admin",
                "password": "Password",
                "port": 22,  # SSH port if you have custom port you can use it
                "secret": "secret",  # Enable password
            }
            ssh = ConnectHandler(**cisco_devices)
            ssh.enable()
            runningconfig = ssh.send_command("show run")
            # Found hostname from running config.
            host_name = ssh.send_command("show run | in hostname")
            backup_name = host_name.split()

            print(f"---------------Backup_Creating {ip_addr}---------------------")
            # Opening a file for save the configuration.
            backupfile = open(f"{folder_name}/{backup_name[1]}_{ip_addr}", "a")
            backupfile.write(runningconfig)
            # File close
            backupfile.close()
            print(
                f"---------------Backup_Success------------------------------------\n"
            )

        except:
            cisco_devices = {
                "device_type": "cisco_ios",
                "host": ip_addr,
                "username": "admin",
                "password": "Password",
                "port": 22,  # SSH port if you have custom port you can use it
                "secret": "password",  # Enable password
            }
            ssh = ConnectHandler(**cisco_devices)
            ssh.enable()
            runningconfig = ssh.send_command("show run")
            # Found hostname from running config.
            host_name = ssh.send_command("show run | in hostname")
            backup_name = host_name.split()

            print(f"---------------Backup_Creating {ip_addr}---------------------")
            # Opening a file for save the configuration.
            backupfile = open(f"{folder_name}/{backup_name[1]}_{ip_addr}", "a")
            backupfile.write(runningconfig)
            # File close
            backupfile.close()
            print(
                f"---------------Backup_Success------------------------------------\n"
            )
