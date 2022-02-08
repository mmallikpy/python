from netmiko import ConnectHandler
import re
from prettytable import PrettyTable


def device_access(ip):
    global ssh
    cisco_devices = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': 'user',
        'password': 'Password',
        'port': 22,  # SSH port if you have custom port you can use it
        'secret': 'Password',  # Enable password
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

'''



def where_user_connected():
    pass


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

def cpu_usages(ip):
    """
    This function show the current CPU usages.\
    Tested on CAT Switch and ISR router
    """
    device_access(ip)
    output = ssh.send_command('show processes memory', use_textfsm=True)
    process = output[:67]
    Total, Used, Free = re.findall('\d*\d', process)
    outputT = PrettyTable(["Total Pool", "Used", "Free"])
    outputT.add_row([f"{Total}", f"{Used}", f"{Free}"])
    print(f'################ Working on {ip} ################')
    print(outputT)
    print('')


def cable_disconnected(ip):
    device_access(ip)
    output = ssh.send_command('show ip interface br', use_textfsm=True)
    outputTup = PrettyTable(['Interface', 'Cable Down/Up'])
    outputTup.align='l'

    for x in output:
        if x['proto'] == 'up':
            outputTup.add_row([f"{x['intf']}", f"{x['proto']}"])
    print(outputTup)


    #for info in command:
    #    if info["proto"] != "up":
    #        print(info["intf"] + " Is cable disconnected")
# ---------------------------------------------------------------------------------------------------------------------------------------

'''
# It's Example never remove it.
for host in ips:
    neighborsDisplay(host)
'''
ips = ["172.16.200.2"]
for host in ips:
    cable_disconnected(host)
