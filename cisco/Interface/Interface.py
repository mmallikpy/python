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


def where_user_connected():
    pass


def neighborsDisplay(ip):
    """
    This function display cisco router, switch neighbour
    Tested on CAT Switch and ISR router
    """
    device_access(ip)
    output = ssh.send_command('show cdp neighbors detail', use_textfsm=True)

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
    This function show the current CPU usages.
    Tested on CAT Switch and ISR router
    """
    device_access(ip)
    output = ssh.send_command('show processes memory', use_textfsm=True)
    process = output[:67]
    Total, Used, Free = re.findall('\d*\d', process)
    outputT = PrettyTable(["Total Pool", "Used", "Free"])
    outputT.add_row([f"{Total}", f"{Used}", f"{Free}"])
    print(outputT)
    print('')


def up_interface(ip):
    """
    This function show the UP Interface only.
    Tested on CAT Switch and ISR router
    """
    device_access(ip)
    output = ssh.send_command('show ip interface br', use_textfsm=True)
    outputTup = PrettyTable(['Interface', 'CableUp'])
    outputTup.align = 'l'

    for x in output:
        if x['proto'] == 'up':
            outputTup.add_row([f"{x['intf']}", f"{x['proto']}"])
    print(outputTup)

def down_interface(ip):
    """
    This function show the Down Interface only.
    Tested on CAT Switch and ISR router
    """
    device_access(ip)
    output = ssh.send_command('show ip interface br', use_textfsm=True)
    outputTdown = PrettyTable(['Interface', 'CableDown'])
    outputTdown.align = 'l'

    for x in output:
        if x['proto'] == 'down':
            outputTdown.add_row([f"{x['intf']}", f"{x['proto']}"])
    print(outputTdown)

def down_by_admin_interface(ip):
    """
    This function show the administratively down Interface only.
    Tested on CAT Switch and ISR router
    """
    device_access(ip)
    output = ssh.send_command('show ip interface br', use_textfsm=True)
    outputTAdown = PrettyTable(['Interface', 'DownByAdmin'])
    outputTAdown.align = 'l'
    for x in output:
        if x['proto'] == 'down' and x['status'] == "administratively down":
            outputTAdown.add_row([f"{x['intf']}", f"{x['proto']}"])
    print(outputTAdown, '\n')

# ----------------------------------Current Working area-----------------------------------------------------------------------------------------------------

def arpToSwitchPortDescription():
    '''
    device_access(ip)
    output = ssh.send_command('show ip arp', use_textfsm=True)
    arp = PrettyTable(['IP', 'MAC'])
    arp.align = 'l'

    switchip = ['172.16.201.12']

    for x in output:
        arp.add_row([f"{x['address']}", f"{x['mac']}"])
        for swip in switchip:
            device_access(swip)
            get_mac_in_port = ssh.send_command(f"show mac address-table address {x['mac']}", use_textfsm=True)
            print(get_mac_in_port)
    '''

    switchip = ['172.16.201.12']
    for swip in switchip:
        device_access(swip)
        get_mac_in_port = ssh.send_command("show mac address-table address e8d8.d157.a5fd", use_textfsm=True)
        print(get_mac_in_port)
    # print(arp)

# ---------------------------------------------------------------------------------------------------------------------------------------

'''
# It's Example never remove it.
for host in ips:
    neighborsDisplay(host)
'''
ips = ["172.16.200.3"]
for host in ips:
    print(f'################ Working on {host} ################')
    # neighborsDisplay(host)
    # neighborToPortDescription(host)
    # cpu_usages(host)
    # up_interface(host)
    # down_interface(host)
    # down_by_admin_interface(host)
arpToSwitchPortDescription()



