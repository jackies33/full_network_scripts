
import logging
import getpass
import re
import paramiko
import time

ip = '10.100.3.77'
user1 = input("login: ")
pass1 = getpass.getpass("password: ")
cmnd1= 'config vdom \n\n'   #Commands
cmnd2= 'show firewall policy \n\n'  #Commands
cmnd3= 'show full-configuration \n\n'  #Commands
cmnd4= 'config firewall policy \n\n'   #Commands
cmnd5= 'set service "DNS" "FTP" "FTP_GET" "FTP_PUT" "RDP" "SAMBA" "SMB" "SSH" "TELNET" \n\n'  #Commands
cmnd6= 'next \n\n'   #Commands
cmnd7= 'end \n\n' #Commands
cmnd8= '\n\n'
fail=''
output2=''
my_file1=open('logging_paramiko2.txt' , 'w')   # logging file for terminal print
my_file2=open('vdoms_where_dns_and_without_polisy.txt', 'w')   #logging file for which target in every iteration
my_file3=open('which_services_in_policy.txt','w')   # for more information about target
only_dns1=''
only_dns2=''
only_dns3=''
which_service=''
logging.getLogger("netmiko").setLevel(logging.WARNING)   # logging for connection
logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)
start_msg = '===> {} Connection: {}'
received_msg = '<=== {} Received:   {}'
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,
            username=user1,
            password=pass1,
            look_for_keys=False )
ssh1 = ssh.invoke_shell()
while True:
 try:
   with open('list1.txt') as f:     #Start of iteration with lines from file
      lines = f.readlines()
      for lin1 in lines:
         lin2 = lin1.split("edit ")
         lin3 = lin2[1]
         for lin4 in lin3:
            lin4 = lin3.split('\n')
         lin5 = lin4[0]
         time.sleep(1)
         ssh1.send(cmnd1)
         ssh1.send(f'{lin1}\n\n')
         time.sleep(1)
         ssh1.send(cmnd2)
         time.sleep(2)
         output1=(ssh1.recv(9999999).decode("utf-8"))
         print(output1)
         time.sleep(1)
         edit1 = re.findall(r'edit \d+\s+set name "Deny Public services"', output1)
         print(edit1)
         time.sleep(2)
         if edit1 == []:
             only_dns1 = (f'{only_dns1} in "{lin5}"- not find a policy with name - "Deny Public services"\n')
             print(f'in "{lin5}" not find a policy with name - "Deny Public services"')
             ssh1.send(cmnd7)
             ssh1.send(cmnd7)
             ssh1.send(cmnd8)
             del (lin5)
             continue
         f1=''
         time.sleep(1)
         for c1 in edit1:
             f1 = str(c1)
         edit2 = f1.split('set name "Deny Public services"')
         edit3 = edit2[0]
         print(edit3)
         ssh1.send(cmnd8)
         ssh1.send(cmnd4)
         ssh1.send(cmnd8)
         time.sleep(1)
         ssh1.send(edit3)
         ssh1.send(cmnd8)
         time.sleep(1)
         ssh1.send(cmnd3)
         ssh1.send(cmnd8)
         time.sleep(1)
         output2 = (ssh1.recv(9999999).decode("utf-8"))
         #print(output2)
         time.sleep(1)
         set_service1  = re.findall(r'set service [\S+ ]*', output2)
         set_service2 = set_service1[0]
         time.sleep(0.5)
         print(set_service2)
         ssh1.send(cmnd8)
         only_dns3 = (f'{only_dns3} in "{lin5}"  was these services --> {set_service2}')
         if set_service2 == 'set service "DNS"':
             time.sleep(0.5)
             ssh1.send(cmnd5)
             time.sleep(0.5)
             ssh1.send(cmnd6)
             ssh1.send(cmnd7)
             ssh1.send(cmnd7)
             ssh1.send(cmnd8)
             only_dns2 = (f'{only_dns2} only DNS in policy in  -  "{lin5}"\n')
             print(f'set config in "{lin5}" is done')
             time.sleep(1.5)
             output3 = (ssh1.recv(9999999).decode("utf-8"))
             #print(output3)
             del (lin5)
         else:

             print(f'in "{lin5}" policy is already done!!!!!')
             time.sleep(1.5)
             ssh1.send(cmnd7)
             ssh1.send(cmnd7)
             ssh1.send(cmnd8)
             del (lin5)

 except IndexError:
  print(f"\n\n\n\n\n\n")
  continue
 break

ssh1.close()
my_file1.write(output1)
my_file1.write(output2)
my_file2.write(only_dns1)
my_file2.write(only_dns2)
my_file3.write(only_dns3)
my_file1.close()
my_file2.close()
my_file3.close()


