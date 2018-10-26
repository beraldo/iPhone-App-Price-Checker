import urllib.request
from bs4 import BeautifulSoup
import re
import os
import sys
import json
import smtplib
import requests
import time

from config import *


def getBaseDir():
    return os.path.dirname(os.path.abspath(__file__))
#########################



def getPriceOfApp(url):
    html = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html, 'html.parser')

    priceTag = soup.find("li", { "class" : "inline-list__item inline-list__item--bulleted" })

    if priceTag == None:
        # erro
        return False


    # price = re.sub('[^0-9.,]', '', priceTag.string)
    price = priceTag.string

    matches = re.match("(gr.tis|free)", price, re.I)

    if matches != None:
        # app is free
        price = 0.0
    else:
        price = re.sub('[^0-9.,]', '', price)

    return float(price)
##########################################



def loadConfig():
    global VARS_FILENAME
    global configVars

    VARS_FILENAME = getBaseDir() + "/" + VARS_FILENAME

    if not os.path.isfile(VARS_FILENAME):
        print("File {0} does not exist".format(VARS_FILENAME))
        sys.exit(-1)

    f = open(VARS_FILENAME, 'r')
    configVars = json.load(f)
    f.close()

    return configVars
##########################################



def sendEmail(msg):
    # configVars = loadConfig()
    global configVars

    headers = [
        'From: {0} <{1}>'.format(configVars['FROM_NAME'], configVars['FROM_EMAIL']),
        'Subject: {0}'.format(configVars['EMAIL_SUBJECT']),
    ]

    headers.append('')
    headers.append(msg)

    message = "\r\n".join(headers)

    server = smtplib.SMTP_SSL(configVars['SMTP_HOST'], configVars['SMTP_PORT'])
    # server.set_debuglevel(1)
    server.ehlo()
    server.login(configVars['SMTP_USERNAME'], configVars['SMTP_PASSWORD'])
    server.sendmail(configVars['FROM_EMAIL'], configVars['TO_EMAIL'], message)
    server.quit()
##########################################

def sendBoxCarNotification(msg):
    global configVars
    # configVars = loadConfig()

    url = configVars['BOXCAR_NOTIFICATION_URL']

    postData = {
        "user_credentials": configVars['BOXCAR_ACCESS_TOKEN'],
        "notification[source_name]": 'AppsPricesReductions',
        "notification[title]": configVars['EMAIL_SUBJECT'],
        "notification[long_message]": msg,
        "notification[sound]": "magic-coin",
    }

    r = requests.post(url, data = postData)
    
    
