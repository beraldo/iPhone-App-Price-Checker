import urllib.request
from bs4 import BeautifulSoup
import re
import os
import sys
import json
import smtplib

from config import *





def getPriceOfApp( url ):
    html = urllib.request.urlopen( url ).read()
    
    soup = BeautifulSoup( html )

    priceTag = soup.find( "div", { "class" : "price" } )
    price = priceTag.string.replace( '$', '' )

    matches = re.match( "(gr.tis|free)", price, re.I )

    if matches != None:
        # app is free
        price = 0.0

    return float( price )
##########################################



def loadConfig():
    global VARS_FILENAME

    if not os.path.isfile( VARS_FILENAME ):
        print( "File {0) does not exist".format( VARS_FILENAME ) )
        sys.exit( -1 )

    f = open( VARS_FILENAME, 'r' )
    configVars = json.load( f )
    f.close()

    return configVars
##########################################



def sendEmail( msg ):
    configVars = loadConfig()

    headers = [
        'From: {0} <{1}>'.format( configVars['FROM_NAME'], configVars['FROM_EMAIL'] ),
        'Subject: {0}'.format( configVars['EMAIL_SUBJECT'] ),
    ]

    headers.append( '' )
    headers.append( msg )

    message = "\r\n".join( headers )

    server = smtplib.SMTP_SSL( configVars['SMTP_HOST'], configVars['SMTP_PORT'] )
    # server.set_debuglevel(1)
    server.ehlo()
    server.login( configVars['SMTP_USERNAME'], configVars['SMTP_PASSWORD'] )
    server.sendmail( configVars['FROM_EMAIL'], configVars['TO_EMAIL'], message)
    server.quit()
##########################################

