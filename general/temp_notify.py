#!/usr/bin/python

import os,readline,subprocess,time
import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart

source_eamil = 'marcbcrobot@gmail.com'
destination_email =  ['marc_blahblah@gmail.com']
sntp_secret = 'xxxxxxxxxxxxxx'
#TODO move both of these to configuration via confiparser or open/reads

def mainish():
    outsidetemp = subprocess.Popen(f"snmpwalk -v2c -c {snmp_comm} 172.17.1.113 .1.3.6.1.4.1.318.1.1.10.4.2.3.1.5.0.2 | awk '{print $4}'", shell=True, stdout=subprocess.PIPE)
    outsidetemp = outsidetemp.stdout.read().strip()

    while True:
        time.sleep(10)

        outsidetempdiff = subprocess.Popen("snmpwalk -v2c -c {snmp_comm} 172.17.1.113 .1.3.6.1.4.1.318.1.1.10.4.2.3.1.5.0.2 | awk '{print $4}'", shell=True, stdout=subprocess.PIPE)
        outsidetempdiff = outsidetempdiff.stdout.read().strip()

        if outsidetemp == outsidetempdiff:
            result = f'The temperature outside of the  window is: {outsidetemp} Degrees, It has NOT changed!!'
            print(result)
            mailnotify(result)
        else:
            result = f'!!!!Temp has changed!!!!! The new temperature  outside of the  window is: {outsidetemp}  Degrees'
            print(result)
            mailnotify(result)
            outsidetemp = outsidetempdiff


def mailnotify(result):
    
    fromadd = source_email
    toaddr = destination_email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromadd, sntp_secret)
    msg = MIMEMultipart() 
    msg['From'] = fromadd
    msg['To'] = toaddr
    msg['Subject'] = "Marc's Weather update!!"
    body = "WEATHER UPDATE: {result}"
    msg.attach(MIMEText(body))
    text = msg.as_string()

    server.sendmail(fromadd, toaddr, text)
    server.quit()
    return 



mainish()
