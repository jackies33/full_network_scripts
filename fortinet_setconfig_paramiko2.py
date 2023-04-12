
import logging
import getpass
import re
import paramiko
from paramiko_expect import SSHClientInteraction
import time



ip = input('ip address: ')
user1 = input('username: ')
pass1 = getpass.getpass('password: ')
cmnd1= 'config vdom\n'
cmnd2= 'show firewall policy\n'
lines= open('list1.txt')
my_file1=open('list_of_out.txt', 'w')
out1=''
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,
            username=user1,
            password=pass1,
            look_for_keys=False )
ssh1 = ssh.invoke_shell()


for lin1 in lines:
    try:
         time.sleep(1)
         ssh1.send('\n\n')
         ssh1.send('end')
         ssh1.send('\n\n')
         ssh1.send(f'{cmnd1}\n')
         time.sleep(1)
         ssh1.send(f'{lin1}\n')
         ssh1.send(f'{cmnd2}\n')
         time.sleep(1)
         output1=(ssh1.recv(65535).decode("utf-8"))
         v1 = re.findall(r'set dstintf "v\d+', output1)
         print(v1)
         if v1 == []:
           out1=out1+'\n'+lin1
         v2 = v1[0]
         v3 =v2.split('set dstintf "v')
         target1 = v3[1]
         emac1 = re.findall(r'set dstintf "v\d+-emac-\d+', output1)
         emac2 = emac1[0]
         emac3 = emac2.split(f'set dstintf "v{target1}-emac-')
         target2 = emac3[1]
         time.sleep(1)
         ssh1.send('\n')
         time.sleep(1)
         ssh1.send('                  config firewall local-in-policy\n')
         ssh1.send(' edit 1\n')
         ssh1.send(f' set intf "v{target1}-emac-{target2}"\n')
         ssh1.send(' set srcaddr "all"\n')
         ssh1.send(' set dstaddr "all"\n')
         ssh1.send(' set service "BGP"\n')
         ssh1.send(' set schedule "always"\n')
         ssh1.send(' next\n')
         ssh1.send(' end\n')
         ssh1.send(' end\n')
         time.sleep(1)
         output2 = (ssh1.recv(65535).decode("utf-8"))
         print(output2)
         target3 = re.findall("(local-in-policy)\s#\s\w+", output2)
         print(target3)
    except IndexError as e:
        print(f"\n\n\n{e}\n\n\n")
        continue
out2='Out of policy:\n' + out1
my_file1.write(out2)
my_file1.close()
ssh.close()


