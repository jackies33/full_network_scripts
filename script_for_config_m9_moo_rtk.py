import pandas as pd
import time

my_file1 = open('config_interfaces.cfg', 'w')
my_file2 = open('config_bgp_m9.cfg', 'w')
my_file3 = open('config_vpn_m9.cfg', 'w')

text1=''
text2='bgp 3.7283\n '
text3=''
data = pd.read_csv ('rtk-shcool-m9.csv', encoding='utf8' ,  sep=',' , usecols=['punkt' , 'lan_m9_rtk' , 'lan_m9_eimts' ,'vlans'])
df = pd.DataFrame(data)
count_list1= df.shape[0]

for m in range(count_list1):
     i1=df.lan_m9_rtk[m]
     i2=df.lan_m9_eimts[m]
     i3=int(df.vlans[m])

     if i3 <= 999:
           text1=text1+(f'\n\n\ninterface Eth-Trunk50.{i3} \n vlan-type dot1q {i3} \n '
                        f'ip binding vpn-instance mo-oo-rtk-espd-0{i3} \n ip address {i2} 255.255.255.252')
           text2 = text2 + (f'\n\n\n ipv4-family vpn-instance mo-oo-rtk-espd-0{i3} \n  maximum load-balancing 2 '
                            f'\n  peer {i1} as-number 12389 \n  peer {i1} connect-interface Eth-Trunk50.{i3} '
                            f'\n  peer {i1} public-as-only force \n  peer {i1} route-policy pl-mo-oo-rtk-espd-as12389-in import'
                            f' \n  peer {i1} route-policy pl-mo-oo-rtk-espd-as12389-out export')
           text3=text3+(f'\n\n\n ip vpn-instance mo-oo-rtk-espd-0{i3} \n  ipv4-family \n   apply-label per-instance'
                        f' \n   vpn-target 105:3010510{i3} export-extcommunity \n   vpn-target 105:3010510{i3} import-extcommunity '
                        f'\n   vpn-target 105:3010{i3} import-extcommunity')
      
     else:
           text1=text1+(f'\n\n\ninterface Eth-Trunk50.{i3} \n vlan-type dot1q {i3} \n ip binding vpn-instance mo-oo-rtk-espd-{i3}'
                        f' \n ip address {i2} 255.255.255.252')
           text2=text2+(f'\n\n\n ipv4-family vpn-instance mo-oo-rtk-espd-{i3} \n  maximum load-balancing 2 '
                        f'\n  peer {i1} as-number 12389 \n  peer {i1} connect-interface Eth-Trunk50.{i3} '
                        f'\n  peer {i1} public-as-only force \n  peer {i1} route-policy pl-mo-oo-rtk-espd-as12389-in import '
                        f'\n  peer {i1} route-policy pl-mo-oo-rtk-espd-as12389-out export')
           text3=text3+(f'\n\n\n ip vpn-instance mo-oo-rtk-espd-{i3} \n  ipv4-family \n   apply-label per-instance'
                        f' \n   vpn-target 105:301051{i3} export-extcommunity \n   vpn-target 105:301051{i3} import-extcommunity '
                        f'\n   vpn-target 105:301{i3} import-extcommunity')

my_file1.write(text1)
my_file1.close()
my_file2.write(text2)
my_file2.close()
my_file3.write(text3)
my_file3.close()
