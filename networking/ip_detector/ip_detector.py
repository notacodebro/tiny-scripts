#!/usr/bin/env python3

import time
import datetime
import requests
import configparser 
import json


config = configparser.ConfigParser()
config.read('config')
log_name = config.get('CONFIGURATION', 'LOG_NAME')
pri_ip_url = config.get('CONFIGURATION', 'PRI_IP_URL')

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def ip_detect(): 
    _url = pri_ip_url
    try:
        ip = requests.get(_url, timeout=5)
        ip = json.loads(ip.text)['ip']
        return ip
    except requests.exceptions.ReadTimeout:
        print('Error: connection timed out, try again')
    except requests.exceptions.ConnectionError:
        print('Error: check that URL is valid')

def logger(ip):
    _log_name = log_name
    _url = pri_ip_url
    try:
        time = datetime.datetime.now()
        outfile = open(_log_name, 'a')
        outfile.writelines(f"IP_LOG::{time}::IP Address::{ip}::url::{_url} \n")
        return True
    except Exception as Error:
        print(f'Error in logger: {Error}')
        return False

def ip_compare():
    _log_name = log_name
    ip_comp = open(_log_name, 'r')
    #ip_comp = readlinesl() #TODO Complete this function

def main():
    ip = ip_detect()
    status = logger(ip)
    if status == True:
        print('log written')
    print(f'IP Address: {Colors.OKBLUE}{ip}{Colors.END}')
    ip_compare()

if __name__ == '__main__':
    main()

   

