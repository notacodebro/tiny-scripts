#!/usr/env/bin python2

import argparse, os, sys, time
from netmiko import ConnectHandler

"""--------------
This script can be used automated by using crontab. The following is an example
*/2 * * * * /usr/bin/python /home/marc/scripts/auto-bounce/autobounce.py -H 172.17.1.104 -O cisco_ios -p 20 

This example executes this script every 2 minutes against device: 172.17.1.104 
---------------"""


def reset_interface(device, ip, port, username, password):
    config_commands = [ 'interface gig0/'+port,
                        'shutdown',
                        'no shutdown',
                    ]
    print '-*'*25
    print '-*\t\texecuting bounce now''\t\t-*'
    print '-*'*25
    net_connect = ConnectHandler(device_type=device, ip=ip, username=username, password=password)
    orig_reset = net_connect.send_command('show int gig0/'+port+' | inc resets')
    orig_reset = orig_reset.split()
    net_connect.send_config_set(config_commands)
    confirmation = net_connect.send_command('show int gig0/'+port+' | inc resets')
    confirmation = confirmation.split()
    sys.stdout =  open('autobounce.log','a')
    print '-'*24
    ts = time.time()
    ftime = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(ts))
    print ftime
    print '-'*24
    if confirmation[5] > orig_reset[5]:
        print 'Interface: Gig0/'+port
        print 'Interface bounced: Yes'
    else:
        print 'Interface bounced: No'
    print 'Original interface resets:',orig_reset[5]
    print 'New interface resets:',confirmation[5]
    print '\n\n'

def main():
    username = 'radmin'
    password = 'xxxxxxx'
    #TODO move this to configuration or inputs
    parser = argparse.ArgumentParser()                                                                        
    parser.add_argument('-H', required=True,  help='Define host to run the tool against')                     
    parser.add_argument('-O', required=True,  help='Which OS is the target host')                     
    parser.add_argument("-p", help="Destination switchport on device")                                        
    args = parser.parse_args() 
    ip = args.H
    device = args.O
    port = args.p
    reset_interface(device, ip, port, username, password)
    
if __name__ == '__main__':                                                                                    
        main()  
