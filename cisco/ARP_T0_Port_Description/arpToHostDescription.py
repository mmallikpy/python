from netmiko import ConnectHandler
import re, socket
from prettytable import PrettyTable


def device_access(ip):
    global ssh
    cisco_devices = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": "userName",
        "password": "Password",
        "port": 22,  # SSH port if you have custom port you can use it
        "secret": "Password",  # Enable password
    }
    ssh = ConnectHandler(**cisco_devices)


def arpToSwitchPortDescription(ip):

    device_access(ip)
    output = ssh.send_command("show ip arp", use_textfsm=True)

    # IP and MAC save in a File from Gateway.
    macIpSave = open("macip.txt", "w")
    for x in output:
        macIpSave.write(f"{x['address']} {x['mac']}\n")
    macIpSave.close()

    # Search MAC in switches
    swli = ["172.16.1.2", "172.16.1.3", "172.16.1.4"]
    for x in swli:
        print("*" * 10, f"{x}", "*" * 10)
        device_access(x)  # Login a switch
        interfaces = ssh.send_command("show interfaces status", use_textfsm=True)

        # Access port find and add accessPorts list
        accessPorts = []
        finalAccessPorts = []
        for y in interfaces:
            mac_count = 0
            get_mac = ssh.send_command(
                f"show mac address-table interface {y['port']}", use_textfsm=True
            )
            # print(f"---------{y['port']}--------------")
            try:
                for mac in get_mac:
                    # print(mac['destination_address'])
                    mac_count += 1
            except:
                pass

            if mac_count == 1:
                # print("Found ", y['port'])
                accessPorts.append(f"{y['port']}")
            else:
                pass

        for inter in accessPorts:
            output = ssh.send_command(
                f"show running-config interface {inter}", use_textfsm=True
            )
            if " switchport mode trunk" not in output:
                finalAccessPorts.append(inter)

        print(finalAccessPorts)

        fileRead = open("macIp.txt", "r")
        x = fileRead.readlines()
        for line in x:
            ip, mac = line.split(" ")
            mac_from_file = mac.strip()
            ip_from_file = ip.strip()

            for interf in finalAccessPorts:
                macinter = ssh.send_command(
                    f"show mac address-table interface {interf}", use_textfsm=True
                )
                for mac_from_inter in macinter:

                    if mac_from_file == mac_from_inter["destination_address"]:
                        print(interf, ip.strip(), mac_from_file)
                        print(ip_from_file)
                        try:
                            print(socket.gethostbyaddr(ip_from_file))
                        except:
                            print(f"{ip.strip()}", "Is not linux or Windows")

        fileRead.close()


ips = ["172.16.1.20"]

for host in ips:
    arpToSwitchPortDescription(host)
