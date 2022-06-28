from examples.example import DisableBiller
from nv9biller import Biller, BillerChannel, BillerEvent,ssp
import time
from datetime import datetime
import os



biller = Biller("COM1")
def getLogFileName():
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y")
    return dt_string
def getLessthan(key,arr):
    lesser = []
    for i in arr:
        if i <= key:
            lesser.append(str(i))
    return lesser

def getAllowedNotes(b,canAccept):
    channels = {
        "5":b.CH_0,
        "10":b.CH_1,
        "20":b.CH_2
    }
    notes = []
    for note in canAccept:
        notes.append(channels[note])
    return notes
def disableBiller():
    global biller
    print("DISABLING")
    biller.display_disable()
    print("DISABLED")
    biller.disable()
   
   

def enableBiller():
    global biller
    print("ENABLING")
    biller.display_enable()    
    biller.enable()   
    print("READY")
    
def getJWP(port,remaining,canAccept):
    global biller
    previous_status = ""
    amount_credited = "0.0"
    
    
    allowed_notes =getAllowedNotes(biller,canAccept)
    #print('-------------------')
    #print('Biller test program')
    #print('SN: {:08X}'.format(biller.serial))
    #print('--------------------')
    #print('Enabling biller...')
    allowed_notes = [Biller.CH_0,Biller.CH_10]
    biller.channels_set(allowed_notes)
    biller.display_enable()
    biller.enable()

    while True:
        i = input("DISABLE BILLER ON DEMAND ?")
        if i == "0":
            disableBiller()
        else:
            enableBiller()
    
    
    f = open(getLogFileName()+".txt",'a')
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    str_log = "["+dt_string+"] Ready"
    while True:
        try:                    
            events = biller.poll()
            for event in events:
                e =str(event) 
                if e != previous_status:
                    previous_status = e
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    str_log = "["+dt_string+"] "+str(event)
                    print(str_log)
                    f.write(str_log+"\n")
                    
                    if "Credit" in e:
                        r = e.split("->")[1].split()
                        
                        amount_credited = r[0]
                        biller.disable()
                        biller.display_disable()
                        f.close()
                        return amount_credited  
                else:               
                    pass
        except Exception as exp:
            print('Disabling biller...',exp)
            biller.disable()
            biller.display_disable()
            biller.channels_set(None)
            break
total_notes = [5,10,20,50,100,200,500]
total = 10
remaining = 10
'''while remaining >0:
    remaining = total - int(float(getJWP("COM1",str(remaining),getLessthan(remaining,total_notes))))
'''
getJWP("COM1","0",["10"])