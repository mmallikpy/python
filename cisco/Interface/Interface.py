from netmiko import ConnectHandler
import json
from pprint import pprint
import re

def device_access(ip):
    global ssh
    cisco_devices = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': 'userName',
        'password': 'Password',
        'port': 22,  # SSH port if you have custom port you can use it
        'secret': 'Secret',  # Enable password
    }

    ssh = ConnectHandler(**cisco_devices)

'''
def up_interface(command):
    # Show the configured and up interface.
    for info in command:
        if info["ipaddr"] != "unassigned" and info["status"] == "up" and info["proto"] == "up":
            print("Interface " + info["intf"] + " Is up,", "And Configured IP is " + info["ipaddr"])


def admin_down_interface(command):
    for info in command:
        if info["status"] != "up" and info["proto"] != "up":
            print(info["intf"] + " Is disconnected or Admin down this port")


def cable_disconnected(command):
    for info in command:
        if info["proto"] != "up":
            print(info["intf"] + " Is cable disconnected")


def where_user_connected():
    pass
'''

def neighborsDisplay(ip):
    """
    This function display cisco router, switch neighbour
    Tested on CAT Switch and ISR router
    """
    device_access(ip)
    output = ssh.send_command('show cdp neighbors detail', use_textfsm=True)
    print(f'################ {ip} ################')

    for x in output:
        print("Local Device :- ")
        print("\t", "From-Port\t:\t", x['local_port'])

        print("Remote Device :- ")
        print("\t", "HostName\t:\t", x['destination_host'])
        print("\t", "MGMT-IP\t:\t", x['management_ip'])
        print("\t", "To-Port\t:\t", x['remote_port'])
        print("\t", "Model\t\t:\t", x['platform'])
        print("")

def neighborToPortDescription(ip):
    """
    This function will collect the cdp neighbour and set the port description.
    Tested on CAT Switch and ISR router
    """
    device_access(ip)
    output = ssh.send_command('show cdp neighbors detail', use_textfsm=True)
    print(f'################ Working on {ip} ################')

    for x in output:
        dest_host = x['destination_host']
        dest_ip = x['management_ip']
        remote_port = x['remote_port']
        description = (dest_host + '_' + dest_ip + '_' + remote_port)   # It's ready the description.
        ssh.send_config_set([f"interface {x['local_port']}", f"description {description}"])  # A Command list
        print("Success interface ", x['local_port'])
        ssh.send_command("do wr")
    print("")

# ---------------------------------------------------------------------------------------------------------------------------------------
def cpu_usages(ip):
    device_access(ip)
    output = ssh.send_command('show processes memory', use_textfsm=True)
    # result = pprint(output.split("\n"))
    process = output[:67]
    print(process)
    Toral, Used, Free = re.findall('\d*\d', process)
    print(Toral)
    '''
    total = process.split("  ")
    for x in total:
        if x != total[0]:
            print(x.split(" "))
    '''

'''
# It's Example never remove it.
for host in ips:
    neighborsDisplay(host)
'''

ips = ["172.16.201.12"]
for host in ips:
    cpu_usages(host)
