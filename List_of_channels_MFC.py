import re
import yaml
import logging
from netmiko import ConnectHandler , NetMikoAuthenticationException, NetMikoTimeoutException
import csv
from paramiko.ssh_exception import SSHException
import getpass
from datetime import datetime

#setup logger settings
logging.getLogger("netmiko").setLevel(logging.WARNING)
logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)


def count_chennels_bgp(command):

    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
#creates file *csv and setup settings for save data about numbers of mfc and how many channels in them
    file1 = open("peer-mfc.csv", mode="w", encoding='utf-8')
    file_writer = csv.writer(file1, delimiter=",", lineterminator="\r")
    file_writer.writerow(["Number of EO MFC", "Count l2 channels"])
    login = input('Login: ')
    password = getpass.getpass('Password:')
    with open('ip-mfc.yaml') as f: #file for load ip addresses for conections
        net1 = yaml.safe_load(f)
    for device in net1['ip']:
#template for connections
         host1 = {

               "host": device,

               "username": login,

               "password": password,

               "device_type": "huawei",

               "global_delay_factor": 0.5,
         }
         try:
              with ConnectHandler(**host1) as net_connect:
                     logging.info(start_msg.format(datetime.now().time(), device))  #start of logs
                     output = net_connect.send_command(command, delay_factor=.5) #command result
                     target1 = re.findall(r"10.100.168.\d+", output) #search our local router bgp id
                     f1 = ""
                     for t1 in target1:
                         f1=str(t1)
                     f2 = f1.split('10.100.168.')
                     f3 = f2[1]                    #leave only last octet from ip address(mfc number)
                     target2 = output.split()
                     count = 0
                     for i2 in target2:   #search lines where have needed word and count them
                         if i2 == 'Established':
                              count = count + 1
                              count2 = str(count)
                     file_writer.writerow([f3, count2])
                     net_connect.disconnect()
                     print('Complete MFC:', f3)
                     logging.info(received_msg.format(datetime.now().time(), device))       #finish logging
         except (SSHException, NetMikoAuthenticationException, NetMikoTimeoutException):   #exceptions
                print('\n\n not connect to ' + device + '\n\n')
                continue

    print('\n\n\n Ready! \n\n\n')
    file1.close()
    return(file1)


print(count_chennels_bgp('display bgp vpnv4 all peer'))  # calling funcion







