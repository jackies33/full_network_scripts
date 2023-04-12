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
my_file = open('config_voip.cfg', 'w')
my_file.write('\n\nconfig for AR\n\n')
login = input('Login: ')
password = getpass.getpass('Password: ')
number_mfc=input("number of mfc(without zero(0): ")
ip_mfc=(f'10.100.169.{number_mfc}')
ip_net_for_voip=ipaddress.IPv4Network(f'10.149.{number_mfc}.0/24')#setup for network voip in AR configuretion
list_subnet=list(ip_net_for_voip.subnets(prefixlen_diff=1))
subnet_500 = list_subnet[1]
subnet_501 = list_subnet[0]
ip_address_501 = (list(subnet_501.hosts())[-1])
ip_address_500 = (list(subnet_500.hosts())[-1])
ip_range_start_501 = (list(subnet_501.hosts())[1])
ip_range_start_500 = (list(subnet_500.hosts())[0])
ip_range_end_501 = (list(subnet_501.hosts())[-2])
ip_range_end_500 = (list(subnet_500.hosts())[-2])
subnet_500_str = str(subnet_500)
subnet_501_str = str(subnet_501)
voip_phones_prefix = subnet_500_str.split('/25')[0]
mfc_voip_prefix = subnet_501_str.split('/25')[0]
ip_ats = (list(subnet_501.hosts())[0])
ip_net_voip5 = str(ip_net_for_voip)
ip5=ip_net_voip5.split('/24')[0]

while True:
   try:
           bool1 = input(f'Its correct address for voip-ats?-> {ip_ats} "yes" or "no" : ')
           if bool1 == 'yes':
                 break
           elif bool1 == 'no':
                 ip_ats = ipaddress.ip_address(input('Enter the correct address for voip-ats: '))
                 break
           else:
                 print('Enter "yes or "no"')
   except ValueError:
    print(f'address is invalid for IPv4:, {ip_ats}!!!')
    continue


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
                     display2 = net_connect.send_command_timing('display interface brief',read_timeout=10, cmd_verify=False)#send commands "display" for search
                     time.sleep(0.5)
                     interface1 = re.findall(r"\S+261", display2)#parcing
                     for c2 in interface1:
                         f3= str(c2)
                     typeint = f3.split("261")
                     t2 = str(typeint[0])
                     display3 = net_connect.send_command_timing('display current-configuration configuration bgp',read_timeout=10, cmd_verify=False)#send commands "display" for search
                     time.sleep(0.5)
                     vpn_instance1 = re.findall(r"ipv4-family vpn-instance mfc-ip-phone-\d+", display3)#parcing
                     for c3 in vpn_instance1:
                         f5= str(c3)
                     vpn_instance2 = f5.split('ipv4-family vpn-instance mfc-ip-phone-')
                     mfc_voip_vrf = str(vpn_instance2[1])
                     if t2 == 'Vlanif' :
                             conf_interface500 = (f'\ninterface Vlanif500 \nundo dhcp select interface \ny \nq \nundo interface Vlanif500 \ninterface Vlanif 500 \nip binding vpn-instance voip-phones \ntcp adjust-mss 1452 \nip address {ip_address_500} 25 \ndhcp select interface \ndhcp server ip-range {ip_range_start_500} {ip_range_end_500} \ndhcp server lease day 8 hour 0 minute 0 \ndhcp server domain-name dp.mosreg.ru \ndhcp server option 242 hex 4D4349504144443D31302E34392E392E33302C4D43504F52543D313731392C48545450535256523D31302E34392E3132352E3132392C4C32513D312C4C3251564C414E3D353030 \ndhcp server logging allocation-success renew-success release \ndhcp server conflict auto-recycle interval day 4 hour 0 minute 0')
                             conf_interface501 = (f'\ninterface Vlanif501 \nip binding vpn-instance mfc-ip-phone-{mfc_voip_vrf} \ntcp adjust-mss 1452 \nip address {ip_address_501} 25 \ndhcp select interface \ndhcp server ip-range {ip_range_start_501} {ip_range_end_501} \ndhcp server lease day 8 hour 0 minute 0 \ndhcp server dns-list 10.10.51.1 10.10.52.1 10.10.51.2 10.10.52.2 10.10.51.3 10.10.52.3 \ndhcp server option 150 ip-address {ip_ats}')
                             conf_interface_conturs=('interface Vlanif260 \ndhcp server option 242 hex 4C32513D312C4C3251564C414E3D353030 \ninterface Vlanif261 \ndhcp server option 242 hex 4C32513D312C4C3251564C414E3D353030 \ninterface Vlanif262 \ndhcp server option 242 hex 4C32513D312C4C3251564C414E3D353030')

                     elif t2 == "Eth-Trunk0." :
                             conf_interface500 = (f'\ninterface Eth-Trunk0.500 \nundo dhcp select interface \ny \nq \nundo interface Eth-Trunk0.500 \ninterface Eth-Trunk0.500 \ndot1q termination vid 500 \nip binding vpn-instance voip-phones \ntcp adjust-mss 1452 \nip address {ip_address_500} 25 \ndhcp select interface \ndhcp server ip-range {ip_range_start_500} {ip_range_end_500} \ndhcp server lease day 8 hour 0 minute 0 \ndhcp server domain-name dp.mosreg.ru \ndhcp server option 242 hex 4D4349504144443D31302E34392E392E33302C4D43504F52543D313731392C48545450535256523D31302E34392E3132352E3132392C4C32513D312C4C3251564C414E3D353030 \ndhcp server logging allocation-success renew-success release \ndhcp server conflict auto-recycle interval day 4 hour 0 minute 0')
                             conf_interface501 = (f'\ninterface Eth-Trunk0.501 \ndot1q termination vid 501 \nip binding vpn-instance mfc-ip-phone-{mfc_voip_vrf} \ntcp adjust-mss 1452 \nip address {ip_address_501} 25 \ndhcp select interface \ndhcp server ip-range {ip_range_start_501} {ip_range_end_501} \ndhcp server lease day 8 hour 0 minute 0 \ndhcp server dns-list 10.10.51.1 10.10.52.1 10.10.51.2 10.10.52.2 10.10.51.3 10.10.52.3 \ndhcp server option 150 ip-address {ip_ats}')
                             conf_interface_conturs = ('interface Eth-Trunk0.260 \ndhcp server option 242 hex 4C32513D312C4C3251564C414E3D353030 \ninterface Eth-Trunk0.261 \ndhcp server option 242 hex 4C32513D312C4C3251564C414E3D353030 \ninterface Eth-Trunk0.262 \ndhcp server option 242 hex 4C32513D312C4C3251564C414E3D353030')

                     elif t2 == "GigabitEthernet0/0/2." :
                             conf_interface500 = (f'\ninterface GigabitEthernet0/0/2.500 \nundo dhcp select interface \ny \nq \nundo interface GigabitEthernet0/0/2.500 \ninterface GigabitEthernet0/0/2.500 \ndot1q termination vid 500 \nip binding vpn-instance voip-phones \ntcp adjust-mss 1452 \nip address {ip_address_500} 25 \ndhcp select interface \ndhcp server ip-range {ip_range_start_500} {ip_range_end_500} \ndhcp server lease day 8 hour 0 minute 0 \ndhcp server domain-name dp.mosreg.ru \ndhcp server option 242 hex 4D4349504144443D31302E34392E392E33302C4D43504F52543D313731392C48545450535256523D31302E34392E3132352E3132392C4C32513D312C4C3251564C414E3D353030 \ndhcp server logging allocation-success renew-success release \ndhcp server conflict auto-recycle interval day 4 hour 0 minute 0')
                             conf_interface501 = (f'\ninterface GigabitEthernet0/0/2.501 \ndot1q termination vid 501 \nip binding vpn-instance mfc-ip-phone-{mfc_voip_vrf} \ntcp adjust-mss 1452 \nip address {ip_address_501} 25 \ndhcp select interface \ndhcp server ip-range {ip_range_start_501} {ip_range_end_501} \ndhcp server lease day 8 hour 0 minute 0 \ndhcp server dns-list 10.10.51.1 10.10.52.1 10.10.51.2 10.10.52.2 10.10.51.3 10.10.52.3 \ndhcp server option 150 ip-address {ip_ats}')
                             conf_interface_conturs = ('interface GigabitEthernet0/0/2.260 \ndhcp server option 242 hex 4C32513D312C4C3251564C414E3D353030 \ninterface GigabitEthernet0/0/2.261 \ndhcp server option 242 hex 4C32513D312C4C3251564C414E3D353030 \ninterface GigabitEthernet0/0/2.262 \ndhcp server option 242 hex 4C32513D312C4C3251564C414E3D353030')

                     vrf1=('\nip vpn-instance voip-phones \nipv4-family \nroute-distinguisher 65535:499100 \napply-label per-instance \nvpn-target 65535:499100 export-extcommunity \nvpn-target 65535:499100 import-extcommunity')
                     bgp1= (f'\nbgp {t1} \nipv4-family vpn-instance voip-phones \nnetwork {voip_phones_prefix} 25 \nmaximum load-balancing 2')
                     bgp2= (f'\nipv4-family vpn-instance mfc-ip-phone-{mfc_voip_vrf} \nundo network {ip5} 24 \nnetwork {mfc_voip_prefix} 25 \nmaximum load-balancing 2')
                     vlan_batch=('vlan batch 501')
                     command_list1 = (vlan_batch, vrf1, conf_interface500,conf_interface501,conf_interface_conturs , bgp1,bgp2 )#configuration collection
                     time.sleep(0.5)
                     #print(vlan_batch, vrf1, conf_interface500, conf_interface501, conf_interface_conturs, bgp1, bgp2)
                     send_commands1 = net_connect.send_config_set(command_list1,read_timeout=20 ,cmd_verify=False)# send commands for configuration
                     time.sleep(0.5)
                     send_save1 = net_connect.save_config('save all')#save configuretion
                     net_connect.disconnect()


except (SSHException, NetMikoAuthenticationException, NetMikoTimeoutException):  # exceptions
             print('\n\n not connect to ' + ip_mfc + '\n\n')
except (ReadTimeout):
             print('long time for a reading')

print("\n\nAR configuration is successfull!\n\n")

for text1 in command_list1:
  my_file.write(''.join(str(text1) + '\n'))

t3 = t1.split('650')[1]
ip_mus=(f'10.100.138.{t3}')#ip for connection NE
time.sleep(0.5)
host2 = {

    "host": ip_mus,

    "username": login,

    "password": password,

    "device_type": "huawei",

    "global_delay_factor": 0.5,

    "session_log": 'log_huawei_NE.txt'  # logging in file
}
try:  #Connection and configuration for NE
    with ConnectHandler(**host2) as net_connect:
        time.sleep(0.5)
        logging.info(start_msg.format(datetime.now().time(), ip_mus))  # start of logs
        time.sleep(0.5)
        display = net_connect.send_command('display current-configuration configuration bgp', read_timeout=20)#send commands "display" for search
        target1 = re.findall(r"peer [0-9]+(?:\.[0-9]+){3} default-originate vpn-instance mfc-ip-phone-", display) #parcing
        f1 = ""
        target2 = ''
        for t1 in target1:
            f1 = str(t1)
            f2 = f1.split('mfc-ip-phone-')
            f3 = str(f2[0])
            f4 = f3 + 'voip-phones \n'
            target2 = (f'{target2 + f4}')
        command_list2 = (f'\nbgp 3.7283 \nipv4-family vpnv4 \n{target2} \ncommit \nreturn')#configuration collection
        time.sleep(0.5)
        send_commands2 = net_connect.send_config_set(command_list2, cmd_verify=False)  # send commands for configuration
        time.sleep(0.5)
        #print(send_commands2)
        send_save2 = net_connect.save_config('save')  # save config
        #print(send_save2)
        net_connect.disconnect()
except (SSHException, NetMikoAuthenticationException, NetMikoTimeoutException):  # exceptions
    print('\n\n not connect to ' + ip_mus + '\n\n')
except (ReadTimeout):
    print('long time for a reading')

print("\n\nNE configuration is successfull!\n\n")

my_file.write('\n\n config for NE\n\n')
my_file.write(command_list2)
