#!/usr/bin/env python3
import requests
import re
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

	 

find = '.*STOCK*'
test_dict = {}
def to_dict(parsedp):
	init = iter(parsedp)
	res_dct = dict(zip(init,init))
	return res_dct

def mailnotify(result):

    toaddr = ['']
    fromadd = ''
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromadd, "iiiiiiiiiiid")
    msg = MIMEMultipart()
    msg['From'] = fromadd
    msg['To'] = ", ".join(toaddr) 
    msg['Subject'] = "N64 CONTROLLER UPDATE!!"
    body = f"STOCK STATUS: {result} "
    msg.attach(MIMEText(body))
    text = msg.as_string()

    server.sendmail(fromadd, toaddr, text)
    server.quit()
    return

#url = 'https://www.nintendo.com/store/products/super-nintendo-entertainment-system-controller/'

url = 'https://www.nintendo.com/store/products/nintendo-64-controller/'

response = requests.get(url) 

soup = BeautifulSoup(response.content, "html.parser")


parsed = str(soup.find_all(id="__NEXT_DATA__")[0]).split(',')


parsedp = parsed[3:]

test_dict = to_dict(parsedp)

results_key = ''
results_val = ''
try:
    results_val = str([v for k, v in test_dict.items() if re.match(find, v) ]).split(':')[1]
except:
    pass
try:
    results_key = str([k for k in test_dict if re.match(find, k)]).split(':')[1]
except:
    pass

if re.match('.*IN_STOCK*', results_val or results_key):
    result = 'in stock'
    mailnotify(result)
elif re.match('.*OUT_OF_STOCK*', results_val or results_key ):
    result = 'out of stock'
else:
    result = 'something went wrong, check the script!!'
    mailnotify(result)

