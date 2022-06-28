import json
from socket import timeout
import sys
import time
from datetime import datetime
from examples.models import PLAN
import printer as p
import time
from nv9biller import Biller
import _thread as thread
import threading 
import pymongo
from datetime import timedelta
from flask import Flask, render_template,redirect,request,jsonify,session,abort
from flask_cors import CORS
from models import LOG,TRANSACTION,USER,PLAN

PORT_USED = "COM1"
app = Flask(__name__)
CORS(app)
biller = None
#app.secret_key = 'NV9-BILLER'

DBURL = "mongodb+srv://testUser:testUser@nv9-testing.9azuqdw.mongodb.net/?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(DBURL)
mydb = myclient["NV9-Testing"]
users = mydb["users"]
transactions = mydb["transactions"]
logs = mydb["log"]

def NewLog(log):
    l = LOG()
    l.log  = log
    logs.insert_one(l.toJson())
def NewTransaction(transaction):
    transactions.insert_one(transaction.toJson())

def NewUser(user):
    try:
        users.insert_one(user.toJson())
    except:
        pass
@app.route("/ping-test")
def ping():
    import os
    ip = "8.8.8.8"
    response = os.popen(f"ping {ip}").read()
    res = {}
    if "Received = 4" in response:
        res["status"] = "successfull"
        res["log"] = response
    else:
        res["status"] = "unsuccessfull"
        res["log"] = response
    return res
@app.route("/stacker_stat")
def stat():
    global biller
    if biller is None:
        try:
            biller =Biller(PORT_USED)
        except:
            return "Machine Connection Problem"
    else:
        obj = {
            "serial":biller.serial,
            "counter":biller.counters,
            "stacker_full":False
        }
        if biller.stacker() :
            obj["stacker_full"] = True
        return obj
def Init_Biller():
    global biller
    if biller is None:
        try:
            biller = Biller(PORT_USED)
        except:
            print("Machine Connection Problem")

@app.route("/jwpTimeOut",methods=["GET","POST"])
def TimeOut():
    global biller 
    
    if request.method == "GET":
        f = p.printerTimeout("30","05830021351","JWP","1125","5",{})
        return "2500"
    elif request.method == "POST":
        amt = request.form.get("amount")
        mobile = request.form.get("mobile")
        service = request.form.get("service")
        term = request.form.get("terminal")
        name = request.form.get("profile")
        pr = request.form.get("price")
        valid = request.form.get("validity")
        rem = request.form.get("remaining")
        print((amt,mobile,term,service,term,name,pr,valid))
        pl = PLAN()
        pl.price = pr
        pl.profile = name
        pl.validity = valid
        t = p.printerTimeout(amt,mobile,service,term,rem,pl.toJson())
        transactions.insert_one(t)
        biller.disable()
        biller.display_disable()
        biller.channels_set(None)
        return "0025"


@app.route("/check_reciept/<reciept>",methods=["GET"])
def getDetailVerfication(reciept):
    query = {"receipt_id" : {"$eq":reciept}}
    r = transactions.find_one(query)
    res = {}
    if r is None:
        return res
    else:
        t= TRANSACTION()
        t.TID = r["TID"]
        t.date = r["date"]
        t.time = r["time"]
        t.receipt_id = r["receipt_id"]
        t.service = r["service"]
        t.phone = r["phone"]
        t.pending_amount = r["pending_amount"]
        t.total_payment = r["total_payment"]
        t.plan = r["plan"]
        if int(t.pending_amount) == 0:
            return res
        res = t.toJson()
        return res
def getLogFileName():
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y")
    return dt_string
@app.route("/printLog")
def printLogFile():
    p.printFile(getLogFileName()+".txt")
    return "DONE"
def acceptMoney(port):
    global biller
    amt = "0.00"
    print('-------------------')
    print('Biller test program')
    print('SN: {:08X}'.format(biller.serial))
    print('--------------------')
    print('Enabling biller...')
    biller.channels_set(biller.CH_ALL)

    biller.display_enable()
    biller.enable()
    while True:
        try:         
            events = biller.poll()
            for event in events:
                e =str(event)
                if "Credit ->" in e:
                    r = e.split("->")[1].strip()
                    #p.print(r)
                    amt =r
                    DisableBiller()
                    return amt
                #now = datetime.now()
                #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                #print("["+dt_string+"]",event)
            
            time.sleep(0.2)
        except:
            print('Disabling biller...')
            biller.disable()
            biller.display_disable()
            biller.channels_set(None)
            break
    return amt




@app.route("/disable-biller")
def DisableBiller():
    global biller
    biller.disable(); 
    biller.display_disable() 
    biller.channels_set(None)
    return "DONE"
@app.route("/enable-biller")
def enableBiller():
    global biller
    biller.channels_set(biller.CH_ALL)
    biller.display_enable()   
    biller.enable()      

    return "DONE"
@app.route("/jwp-money/",methods = ["GET"])
def handleJWPMoney():
    return getJWP(PORT_USED)

def getLessthan(key,arr):
    lesser = []
    for i in arr:
        if i <= key:
            lesser.append(str(i))
    return lesser



def getJWP(port):
    global biller
    notes_avail = [5,10,20,50,100,200,500]
    previous_status = ""
    amount_credited = "0.0"  
    allowed_notes =[biller.CH_0,biller.CH_1,biller.CH_2]
    #print('-------------------')
    print('Biller test program')
    print('SN: {:08X}'.format(biller.serial))
    #print('--------------------')
    #print('Enabling biller...')
    biller.channels_set(allowed_notes)
    biller.display_enable()   
    biller.enable() 
    f = open(getLogFileName()+".txt",'a')
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  
    str_log = "["+dt_string+"] Ready"
    f.write(str_log+"\n")
    NewLog("Ready")
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
                    NewLog(str(event))
                    print(str_log)
                    f.write(str_log+"\n")
                    
                    if "Credit" in e:
                        r = e.split("->")[1].split()                  
                        amount_credited = r[0]
                        DisableBiller()
                        f.close()
                        return amount_credited  
                else:               
                    pass
        except Exception as exp:
            print('Disabling biller...',exp)
            DisableBiller()
            return amount_credited
    DisableBiller()
    biller.channels_set(None)
    return amount_credited


@app.route("/cmdPrint",methods=["GET","POST"])

def testPr():
    commision_applied = ["du","du | extra minutes"]
    if request.method == "GET":
        p.printer("100","0583009340","du | extra hours","0125",True)
        return "152"
    elif request.method == "POST":
        amount = request.form.get("amount")
        mobile = request.form.get("number")
        service = request.form.get("company")
        print("[LOG DATA]",amount,mobile,service)
        c = False
        if service in commision_applied:
            c  = True
        p.printer(amount,mobile,service,"0125",c)
        return "521"

@app.route("/print",methods=["GET"])
def printData():
    return render_template("./home_print_test.html")
@app.route("/voucherPrint",methods=["GET","POST"])
def printVoucher():
    if request.method  ==  "GET":
        q =  p.voucher("338","11590","115645614515","30-Days","30","971583009341")
    elif request.method == "POST":
        vc = request.form.get("code")
        pl = request.form.get("profile")
        site = request.form.get("site")
        paid = request.form.get("amount")
        ph = request.form.get("phone")
        serial = "1122"
        q = p.voucher(site,serial,vc,pl,paid,ph)
        transactions.insert_one(q)
        return "221"  
@app.route("/")
def home():
    return"BACK END WORKING"
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/accept-money')
def hello_world():
    moneyaccepted = acceptMoney(PORT_USED)
    return moneyaccepted
# main driver function
def AppRun():
    app.debug = True
    app.run(host="0.0.0.0",port=443, use_reloader=False,ssl_context=("localhost+2.pem","localhost+2-key.pem"))
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    
    threading.Thread(Init_Biller()).start()
    print("Waiting for Biller to INIT")
    while biller is None:
        time.sleep(0.5)
    if biller is not None:
        print("Init Biller Success")
        threading.Thread(AppRun()).start()
        
        
        
    

