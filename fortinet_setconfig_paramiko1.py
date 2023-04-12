
import logging
import getpass
import re
import paramiko
import time

ip = input('ip for connections: ')
user1 = input('username: ')
pass1 = getpass.getpass('password: ')
cmnd1= 'config vdom\n'
cmnd2= 'show firewall policy\n'
fail=''
output2=''
my_file1=open('logging_paramiko1.txt' , 'w')
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,
            username=user1,
            password=pass1,
            look_for_keys=False )
ssh1 = ssh.invoke_shell()
try:
   with open('list1.txt') as f:
      lines = f.readlines()
      for lin1 in lines:
         time.sleep(1)
         ssh1.send(cmnd1)
         ssh1.send(lin1)
         time.sleep(1)
         ssh1.send(cmnd2)
         time.sleep(1)
         output1=(ssh1.recv(65535).decode("utf-8"))
         t1 = re.findall(r'set dstintf "v\d+', output1)
         t2 = t1[0]
         t3 =t2.split('set dstintf "v')
         target1 = t3[1]
         time.sleep(0.5)
         ssh1.send('\n\nconfig firewall local-in-policy\n')
         ssh1.send('edit 1\n')
         ssh1.send(f'set intf "v{target1}-emac-2000"\n')
         ssh1.send('set srcaddr "all"\n')
         ssh1.send('set dstaddr "all"\n')
         ssh1.send('set service "BGP"\n')
         ssh1.send('set schedule "always"\n')
         ssh1.send('next\n')
         ssh1.send('end\n')
         ssh1.send('end\n')
         time.sleep(1)
         output2 = (output2 + ssh1.recv(1024).decode("utf-8"))
         print(output2)
         try:
             e1= re.findall(r'node_check_object fail!', output2)
             e2=e1[0]
             #print(e2)
             if e2 == 'node_check_object fail!':
               fail = (lin1 + '\n')
               print(f'\n\nError input config in vdom -->> {lin1}!\n\n')

         except IndexError:
             continue
except IndexError as e:
    print(f"\n\n\n{e}\n\n\n")


fail1= "Error input config in vdoms:\n" + fail
ssh.close()
print(fail1)
my_file1.write(fail1)
my_file1.close()
ssh.close()

