import ipaddress
import json


def ip_address_gen (net):
      i1 = ipaddress.IPv4Network(net)
      ippool = ''
      for ip in i1:
          ip = str(ip)
          ippool= (ippool + ip + f' \n')
      ippool1 = ippool.split('\n')
      del ippool1[0]
      del ippool1[-1]
      del ippool1[-2]
      return(ippool1)


input3=''

while input3 is not None:
    try:
        input3 = input('please enter ipv4 prefix(for example 10.10.10.0/24) : ')
        break
    except ipaddress.AddressValueError as AddressValueError:
        print(AddressValueError)

list=(ip_address_gen(input3))
my_file=open('ip_gen1.yaml', 'w')
my_file
for item in list:
    my_file.write("%s\n" % item)
my_file.close()
