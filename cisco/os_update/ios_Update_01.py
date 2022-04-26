import os
import logging
from netmiko import ConnectHandler

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def ftp():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user('mn', '12345', '.')
    #authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = '151.25.42.11'
    #handler.passive_ports = range(60000, 65535)
    #logging.basicConfig(filename='/var/log/pyftpd.log', level=logging.INFO)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('', 21)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()

def ios_version_check(ip_addr):

    cisco_devices = {
        'device_type': 'cisco_ios',
        'host': ip_addr,
        'username': 'mithun',
        'password': '',
        'port': 22,                        # SSH port if you have custom port you can use it
        "secret": "",              # Enable password
    }
    ssh = ConnectHandler(**cisco_devices)
    ssh.enable()
    version = ssh.send_command('show bootvar')
    print(version.split(',')[0])



if __name__ == '__main__':
    ios_version_check('172.16.201.12')
