"""
# For this LAB I used. 
    1. eve-ng
    2. netmiko
    3. pandas
    4. Router model and verion : 3700, 12.4(25d).
# My goal
    1. I will give the information in Excel sheet and python script configure the router.

# Step of works.
    1. Configure your router Management IP.
    2. Create a privileges user(15) and Enable the ssh.
    3. Create a Excel sheet like me.
        Note: If you not clear the script please don't change the Excel sheet formate, this script depend on the sheet.
Note: If you want to use this script for your environment, First read the script documentation carefully and try to understand.
      the script after that deploy it.    
"""

from netmiko import ConnectHandler
import pandas as pd

infor_from_file = pd.read_excel('command.xlsx')


def user(ip):
    global ssh
    cisco_devices = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': 'mithun',
            'password': 'XXXXX',
            'port': 22,  # SSH port if you have custom port you can use it
            'secret': 'XXXXXX',  # Enable password
        }
    ssh = ConnectHandler(**cisco_devices)

# Creating command taken data from Excel.

command_list = []
for count in range(len(infor_from_file["MGMT_IP"])):
    if infor_from_file["MGMT_IP"][count]!=0:
        command_list.append(infor_from_file["MGMT_IP"][count])
        
    else:
        output = infor_from_file["Interface"][count], infor_from_file["IP"][count], infor_from_file["mask"][count], infor_from_file["Description"][count]
        command_list.append(output)


for ip in command_list:
    if type(ip)==str:
        user(ip)    # Passing IP for SSH.      
        print("----------------",ip, "----------------")
  
    if type(ip) == tuple:
        config_command = list(ip)
   
        if '.' in config_command[0]:
            subIntNum = config_command[0].split('.')
            
            # It's configure the subinterface.
            
            print('Configuring : ', config_command[0] )
            print("Configure success\n")
            
            # Bellow line is configure the subinterface IP address. My lab it's need the encapsulation dot1Q if you don't need just remove.
            # f'encapsulation dot1Q {subIntNum[1]}',
            
            command = [f"interface {config_command[0]}", f'encapsulation dot1Q {subIntNum[1]}', f"ip addr {config_command[1]} {config_command[2]}", f"description {config_command[3]}", 'no shutdown', 'do wr']
            ssh.send_config_set(command)
            print(ssh.send_command(f'show run int {config_command[0]}')) # It will show the configured running configuration
            
            """
                It's no shutdown the subinterface main Interface.
            """
            command1 = [f"interface {subIntNum[0]}",'no shutdown']
            ssh.send_config_set(command1)
     
        else:
            """
                It's configure the Interface
            """
            print('Configuring : ', config_command[0] )
            print("Configure success\n")
            
            command2 = [f"interface {config_command[0]}", f"ip addr {config_command[1]} {config_command[2]}", f"description {config_command[3]}", 'no shutdown', 'do wr']
            ssh.send_config_set(command2)
            print(ssh.send_command(f'show run int {config_command[0]}')) # It will show the configured running configuration
            

