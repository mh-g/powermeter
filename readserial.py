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
    if re.match("^1-0:\d.\d.\d\*255\(\d\d\d\d\d\d.\d\d\d\d\*kWh\)$", sentence):
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
        return (obis.group(), value, unit)
    return None, None, None

def updaterrd (paid, excess):
    rrdtool.update(database, "N:%f:%f:%f" % (paid, excess, paid - excess))

# main program

paid = 0.0
prevPaid = paid
excess = 0.0
prevExcess = excess
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
                        if (prevPaid < 0.001):
                            print ("First paid:", paid)
                            prevPaid = paid
                            gotPaid = True
                        if (paid - prevPaid) < 0.1:
                            gotPaid = True
                            prevPaid = paid
                        else:
                            gotPaid = False
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
                        if (prevExcess < 0.001):
                            print ("First excess:", excess)
                            prevExcess = excess
                            gotExcess = True
                        if (excess - prevExcess) < 0.1:
                            gotExcess = True
                            prevExcess = excess
                        else:
                            gotExcess = False
                    except:
                        print ("parse error with excess", valuestr)
                        pass
                    try:
                        if gotPaid:
                            updaterrd (paid, excess)
                    except:
                        print ("Unexpected error with excess:", sys.exc_info()[0])
