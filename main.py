#!/usr/bin/env python

import sys
import os
import json

from config import *
from functions import *

JSON_FILENAME = getBaseDir() + "/" + JSON_FILENAME

# read olde prices
oldPrices = {}
if os.path.isfile( JSON_FILENAME ):
    f = open( JSON_FILENAME, 'r' )
    oldPrices = json.load( f )
    f.close()



jsonArr = {}
msg = []
for name, url in apps.items():
    price = getPriceOfApp( url )

    if name in oldPrices:
        oldPrice = float( oldPrices[name] )
        if price < oldPrice:
            if price == 0.0:
                msg.append( "App {0} is FREE! (before: ${1}): {2}".format( name, oldPrice, url ) )
            else:
                msg.append( "Price reduction for app {0}. From ${1} for ${2}: {3}!!".format( name, oldPrice, price, url ) )
            

    jsonArr[ name ] = price
    

jsonStr = json.dumps( jsonArr )

f = open( JSON_FILENAME, 'w' )
f.write( jsonStr )
f.close()

if len( msg ) > 0:
    msg = "\r\n\r\n\r\n".join( msg )
    sendEmail( msg )
    print( msg )
else:
    print( "no price reductions" )
