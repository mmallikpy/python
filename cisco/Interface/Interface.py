from netmiko import ConnectHandler

def up_interface(command):
    # Show the configured and up interface.
    for info in command:
        if info["ipaddr"] != "unassigned" and info["status"] == "up" and info["proto"] == "up":
            print("Interface " + info["intf"] + " Is up,", "And Configured IP is " + info["ipaddr"])

def admin_down_interface(command):
    for info in command:
        if info["status"] != "up" and info["proto"] !="up":
            print(info["intf"] + " Is disconnected or Admin down this port")

def cable_disconnected(command):
    for info in command:
        if info["proto"] !="up":
            print(info["intf"] + " Is cable disconnected")

#--------------------------------------------------------
cisco_devices = {
            'device_type': 'cisco_ios',
            'host': "172.16.1.2",
            'username': 'mithun',
            'password': 'C1sc0@123',
            'port': 22,                        # SSH port if you have custom port you can use it
            "secret": "C1sc0@123",              # Enable password
}
ssh = ConnectHandler(**cisco_devices)
ssh.enable()


interface = ssh.send_command('show ip interface brief', use_textfsm=True)
#for a in command:
#    print(a)
print("\n")
up_interface(interface)
print("\n")
admin_down_interface(interface)
print("\n")
cable_disconnected(interface)
print("\n")