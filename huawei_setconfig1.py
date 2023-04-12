import time
import re
import logging
from netmiko import ConnectHandler , NetMikoAuthenticationException, NetMikoTimeoutException, ReadTimeout
from paramiko.ssh_exception import SSHException
import getpass
from datetime import datetime
import ipaddress

#setup logger settings
logging.getLogger("netmiko").setLevel(logging.WARNING)
logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)
start_msg = '===> {} Connection: {}'
received_msg = '<=== {} Received:   {}'
login = input('Login: ')
password = getpass.getpass('Password: ')
#ip_mus= input('MUS ip for connection: ')
ip_mfc1=input('number of MFC: ')
ip_mfc=(f'10.100.169.{ip_mfc1}')
ip_prefix=input("ip prefix(example:10.112.200.16/28): ")
ip_prefix1=ip_prefix.split('/28')[0]
ip_interface1 = ipaddress.IPv4Network(ip_prefix)
ippool = ''
for ip in ip_interface1:
    ip = str(ip)
    ippool = (ippool + ip + f'\n')
ippool1 = ippool.split('\n')
ip_interface2=ippool1[-3]

#AR

host1 = {

           "host": ip_mfc,

           "username": login,

           "password": password,

           "device_type": "huawei",

           "global_delay_factor": 0.5,

           "session_log": 'log_huawei_AR.txt'  # logging in file
        }
try:
              with ConnectHandler(**host1) as net_connect:
                     time.sleep(0.5)
                     logging.info(start_msg.format(datetime.now().time(), ip_mfc))  #start of logs
                     display1 = net_connect.send_command('dis bgp vpnv4 all peer')
                     numberas = re.findall(r"Local AS number : \d+", display1)
                     for c1 in numberas:
                         f1=str(c1)
                     f2 = f1.split('Local AS number :')
                     t1=f2[1]
                     #print ('bgp',t1)
                     display2 = net_connect.send_command_timing('display interface brief',read_timeout=10, cmd_verify=False)
                     time.sleep(0.5)
                     interface1 = re.findall(r"\S+261", display2)
                     for c2 in interface1:
                         f3= str(c2)
                     typeint = f3.split("261")
                     t2 = str(typeint[0])
                     #print(t2)
                     if t2 == 'Vlanif' :
                             conf_interface = (f'\ninterface Vlanif 120 \nip binding vpn-instance msr-region \ntcp adjust-mss 1452 \nip address {ip_interface2} 28 \ndhcp select interface \ndhcp server lease day 8 hour 0 minute 0 \ndhcp server dns-list 10.10.51.1 10.10.52.1 10.10.51.2 10.10.52.2 10.10.51.3 10.10.52.3 \ndhcp server domain-name dp.mosreg.ru \ndhcp server option 242 hex 4C32513D312C4C3251564C414E3D353030')

                     elif t2 == "Eth-Trunk0." :
                             conf_interface = (f'\ninterface Eth-Trunk0.120 \ndot1q termination vid 120 \nip binding vpn-instance msr-region \ntcp adjust-mss 1452 \nip address {ip_interface2} 28 \ndhcp select interface \ndhcp server lease day 8 hour 0 minute 0 \ndhcp server dns-list 10.10.51.1 10.10.52.1 10.10.51.2 10.10.52.2 10.10.51.3 10.10.52.3 \ndhcp server domain-name dp.mosreg.ru \ndhcp server option 242 hex 4C32513D312C4C3251564C414E3D353030')

                     elif t2 == "GigabitEthernet0/0/2." :
                             conf_interface = (f'\ninterface GigabitEthernet0/0/2.120 \ndot1q termination vid 120 \nip binding vpn-instance msr-region \ntcp adjust-mss 1452 \nip address {ip_interface2} 28 \ndhcp select interface \ndhcp server lease day 8 hour 0 minute 0 \ndhcp server dns-list 10.10.51.1 10.10.52.1 10.10.51.2 10.10.52.2 10.10.51.3 10.10.52.3 \ndhcp server domain-name dp.mosreg.ru \ndhcp server option 242 hex 4C32513D312C4C3251564C414E3D353030')
                     vrf1=('\nip vpn-instance msr-region \nipv4-family \nroute-distinguisher 108:300 \napply-label per-instance \nvpn-target 108:300 export-extcommunity \nvpn-target 108:300 import-extcommunity')
                     bgp1= (f'\nbgp {t1} \nipv4-family vpn-instance msr-region \nnetwork {ip_prefix1} 28 \nmaximum load-balancing 2')
                     vlan_batch=('vlan batch 120')
                     command_list1 = (vlan_batch, vrf1, conf_interface, bgp1 )
                     #print(vlan_batch, vrf1, conf_interface , bgp1)
                     time.sleep(0.5)
                     send_commands1 = net_connect.send_config_set(command_list1, cmd_verify=False)
                     time.sleep(0.5)
                     send2 = net_connect.save_config('save all')
                     net_connect.disconnect()
except (SSHException, NetMikoAuthenticationException, NetMikoTimeoutException):  # exceptions
             print('\n\n not connect to ' + ip_mfc + '\n\n')
except (ReadTimeout):
             print('long time for a reading')

print("\n\nAR configuration is successfull!\n\n")
#NE

t3 = t1.split('650')[1]
ip_mus=(f'10.100.138.{t3}')
time.sleep(0.5)
host2 = {

    "host": ip_mus,

    "username": login,

    "password": password,

    "device_type": "huawei",

    "global_delay_factor": 0.5,

    "session_log": 'log_huawei_NE.txt'  # logging in file

}
try:
    with ConnectHandler(**host2) as net_connect:
        time.sleep(0.5)
        logging.info(start_msg.format(datetime.now().time(), ip_mus))  # start of logs
        time.sleep(0.5)
        display = net_connect.send_command('display current-configuration configuration bgp', read_timeout=20)
        target1 = re.findall(r"peer [0-9]+(?:\.[0-9]+){3} default-originate vpn-instance mfc-sc-", display)
        f1 = ""
        t4 = ""
        target2 = ''
        time.sleep(1)
        display3 = net_connect.send_command('display current-configuration configuration vpn-instance', read_timeout=20)
        target3 = re.compile(r"ip vpn-instance (minsoc-region|msr-region)")
        target4 = str(target3.findall(display3)[0])
        time.sleep(0.5)
        for t1 in target1:
           f1 = str(t1)
           f2 = f1.split('mfc-sc-')
           f3 = str(f2[0])
           f4 = (f"{f3}{target4} \n")
           target2 = (f'{target2 + f4}')

        command_list1 = (f'\nbgp 3.7283 \nipv4-family vpnv4 \n{target2} \ncommit \nreturn')
        #print(command_list1)
        time.sleep(0.5)
        send1 = net_connect.send_config_set(command_list1, cmd_verify=False)  # connection and send commands
        time.sleep(0.5)
        send2 = net_connect.save_config('save')  # save config
        # print(send1)
        # print(send2)
        net_connect.disconnect()
except (SSHException, NetMikoAuthenticationException, NetMikoTimeoutException):  # exceptions
    print('\n\n not connect to ' + ip_mus + '\n\n')
except (ReadTimeout):
    print('long time for a reading')

print("\n\nNE configuration is successfull!\n\n")





