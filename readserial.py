# Author: https://github.com/mh-g
# Licensed under MIT license

import serial
import re
import rrdtool
import datetime
import sys

# ================================================================
# modify these to suit your needs!
database = "/srv/dev-disk-by-label-DISK1/localdata/powermeter.rrd"
port = serial.Serial ("/dev/ttyUSB0", 115200, timeout=1)
# ================================================================

def parse (sentence):
    obis = re.match("\d-\d*:\d*\.\d*\.\d*", sentence)
    if obis == None:
        return None, None, None
    data = sentence[obis.end() + 5:len(sentence) - 1]
    value = ""
    unit = ""
    if data.find("*") > 0:
        value = data[:data.find("*")]
        unit = data[data.find("*") + 1:]
    else:
        value = data
    print (obis.group(), value, unit)
    return (obis.group(), value, unit)

def updaterrd (paid, excess):
    rrdtool.update(database, "N:%f:%f:%f" % (paid, excess, paid - excess))

# main program

paid = 0.0
excess = 0.0
gotPaid = False
gotExcess = False
while True:
    message = (str) (port.read(2048))
    sentences = re.findall("\d*-\d*\:\d*\.\d*\.\d*\*255\(.*?\)", message)

    for sentence in sentences:
        obis, valuestr, unit = parse (sentence)
        if obis != None:
            if len(unit) > 0:
                if obis == "1-0:1.8.0":
                    try:
                        paid = (float)(valuestr)
                        gotPaid = True
                    except:
                        print ("parse error with paid", valuestr)
                        pass
                    try:
                        if gotExcess:
                            updaterrd (paid, excess)
                    except:
                        print("Unexpected error with paid:", sys.exc_info()[0])


                if obis == "1-0:2.8.0":
                    try:
                        excess = (float)(valuestr)
                        gotExcess = True
                    except:
                        print ("parse error with excess", valuestr)
                        pass
                    try:
                        if gotPaid:
                            updaterrd (paid, excess)
                    except:
                        print ("Unexpected error with excess:", sys.exc_info()[0])
