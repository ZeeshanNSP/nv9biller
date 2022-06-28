from distutils.command.check import HAS_DOCUTILS
import win32ui, win32con,win32print
import datetime
import uuid 
from models import TRANSACTION,VOUCHER

def getfontsize(dc, PointSize):
    inch_y = dc.GetDeviceCaps(win32con.LOGPIXELSX)
    print("[INCHES SIZE]",inch_y)
    return int(-(PointSize * inch_y) / 72)

def printFile(filename):
    hDC = win32ui.CreateDC()
    printer_name = win32print.GetDefaultPrinter ()
    hDC.CreatePrinterDC(printer_name)
    hDC.StartDoc('TESTING DO')
    hDC.StartPage()
    Y = 1
    Y_distance = 30
    fontsize = getfontsize(hDC, 12)
    fontdata = {'name': 'Aerial', 'height': fontsize ,'weight':win32con.FW_NORMAL}
    font = win32ui.CreateFont(fontdata)
    hDC.SelectObject(font)
    hDC.TextOut(5, Y,"                 ** FILE "+filename.split(".")[0]+"**")
    Y += 40


    fontsize = getfontsize(hDC, 9)
    fontdata = {'name': 'Aerial', 'height': fontsize ,'weight':win32con.FW_NORMAL}
    font = win32ui.CreateFont(fontdata)
    hDC.SelectObject(font)
    
    
    f = open(filename,"r")
    f = f.readlines()
    for line in f:
        hDC.TextOut(5, Y,line)
        Y += Y_distance
    hDC.TextOut(5, Y,"--------------------------------------------------------------------------------")
    Y += 40
    hDC.TextOut(5, Y,"============END OF LOG FILE============")
    Y += 40
    hDC.EndPage()   
    hDC.EndDoc() 
    return "Done"

def voucher(site_name,serial,voucher_code,plan,paid,ph):
    hDC = win32ui.CreateDC()
    printer_name = win32print.GetDefaultPrinter ()
    hDC.CreatePrinterDC(printer_name)
    hDC.StartDoc('VOUCHER DOC')
    hDC.StartPage()
    fontsize = getfontsize(hDC, 11)
    fontdata = {'name': 'Aerial', 'height': fontsize ,'weight':win32con.FW_NORMAL}
    font = win32ui.CreateFont(fontdata)
    hDC.SelectObject(font)
    Y = 1
    Y_distance = 30
    hDC.TextOut(10, Y,"          Logo     "+site_name+"      ["+serial+"]")
    Y += Y_distance
    hDC.TextOut(10, Y, " ---------------------------------------------------") 
    Y += Y_distance
    hDC.TextOut(10, Y, "                     Voucher Code")              
    Y += Y_distance
    hDC.TextOut(10, Y, "                     "+voucher_code)              
    Y += Y_distance
    hDC.TextOut(10, Y, " ---------------------------------------------------") 
    Y += Y_distance
    
    hDC.TextOut(10, Y, "                Plan ["+plan+"] ") 
    Y += Y_distance 
    hDC.TextOut(10, Y, " ---------------------------------------------------") 
    Y += Y_distance
    hDC.EndPage()                    
    hDC.EndDoc() 
    v = VOUCHER()
    v.payment=paid
    v.plan = plan
    v.phone = ph
    v.receipt_id=serial
    v.service = site_name
    v.pin = voucher_code
    return v.toJson()
def printer(amount,contact_number,service_name,terminalId,com = False):
    hDC = win32ui.CreateDC()
    printer_name = win32print.GetDefaultPrinter ()
    hDC.CreatePrinterDC(printer_name)
    hDC.StartDoc('TESTING DOC')
    hDC.StartPage()
    fontsize = getfontsize(hDC, 9
    )
    fontdata = {'name': 'Aerial', 'height': fontsize ,'weight':win32con.FW_NORMAL}
    font = win32ui.CreateFont(fontdata)
    hDC.SelectObject(font)
    
    Y = 1
    Y_distance = 30
    hDC.TextOut(10, Y,"Nonstop Payment LLC TIN : 00000025252")
    Y += Y_distance
    hDC.TextOut(10, Y, "Jabel Ali [Here will be the address]") 
    Y += Y_distance
    hDC.TextOut(10, Y, "-----------------------------------------")              
    Y += Y_distance
    now = datetime.datetime.now()
    now = now.strftime("%d-%m-%Y %H:%M:%S %I")
    hDC.TextOut(10, Y, "Date: "+now)              
    Y += Y_distance
    id = str(uuid.uuid1())
    hDC.TextOut(10, Y, "Recipt #: "+id[0:5])              
    Y += Y_distance
    hDC.TextOut(10, Y, "Terminal #: 1234")              
    Y += Y_distance
    hDC.TextOut(10, Y, "Address: Dubai Investment Park First, Jabal Ali")              
    Y += Y_distance
    hDC.TextOut(10, Y, "-----------------------------------------")              
    Y += Y_distance
    #service_name = "etisalat | Prepaid"
    hDC.TextOut(10, Y, "Customer: "+service_name)              
    Y += Y_distance
    hDC.TextOut(10, Y, "Entered Data:")              
    Y += Y_distance
    #contact_number = "0583009340"
    hDC.TextOut(10, Y, "Mobile number: "+contact_number)              
    Y += Y_distance
    amount_accepted = float(amount)
    hDC.TextOut(10, Y, "Accepted: AED "+str(amount_accepted))              
    Y += Y_distance
    commission = 0.00
    Transacted = amount_accepted
    if com == True:
        commission = 1.00
        Transacted  = amount_accepted - commission
    hDC.TextOut(10, Y, "Commision: AED "+str(commission))              
    Y += Y_distance
    hDC.TextOut(10, Y, "Transacted: AED "+str(Transacted) )             
    Y += Y_distance
    hDC.TextOut(10, Y, "-----------------------------------------")              
    Y += Y_distance
    hDC.TextOut(10, Y, "Service provider's support # 090075601")              
    Y += Y_distance
    hDC.TextOut(10, Y, "NonStop Payments Support # 090075601")              
    Y += Y_distance
    hDC.TextOut(10, Y, "Dealer's support # 044448484")            
    Y += Y_distance
    hDC.TextOut(10, Y, "Whatsapp # 0568494189")            
    Y += Y_distance
    hDC.TextOut(10, Y, "Working hours: 09:00-22:00")              
    Y += Y_distance 
  
    hDC.TextOut(10, Y, "Keep the reciept until the payment is confirm!")                        
    Y += Y_distance
    hDC.EndPage()
    hDC.EndDoc() 
    return "Done"
def printCounter(jsonObj):
    hDC = win32ui.CreateDC()
    printer_name = win32print.GetDefaultPrinter ()
    hDC.CreatePrinterDC(printer_name)
    hDC.StartDoc('TESTING DOC')
    hDC.StartPage()
    fontsize = getfontsize(hDC, 9
    )
    fontdata = {'name': 'Aerial', 'height': fontsize ,'weight':win32con.FW_REGULAR}
    font = win32ui.CreateFont(fontdata)
    hDC.SelectObject(font)    
    Y = 1
    Y_distance = 30
    for i in jsonObj:    
        line = f"{i} : {jsonObj[i]}"
        hDC.TextOut(10, Y,line)
        Y += Y_distance
    hDC.EndPage()
    hDC.EndDoc() 
def printerTimeout(amount,contact_number,service_name,terminalId,remaining,plan):
    hDC = win32ui.CreateDC()
    printer_name = win32print.GetDefaultPrinter ()
    hDC.CreatePrinterDC(printer_name)
    hDC.StartDoc('TESTING DOC')
    hDC.StartPage()
    fontsize = getfontsize(hDC, 9
    )
    fontdata = {'name': 'Aerial', 'height': fontsize ,'weight':win32con.FW_REGULAR}
    font = win32ui.CreateFont(fontdata)
    hDC.SelectObject(font)
    
    Y = 1
    Y_distance = 30
    hDC.TextOut(10, Y,"Nonstop Payment LLC TIN : 00000025252")
    Y += Y_distance
    hDC.TextOut(10, Y, "Jabel Ali [Here will be the address]") 
    Y += Y_distance
    hDC.TextOut(10, Y, "-----------------------------------------")              
    Y += Y_distance
    now = datetime.datetime.now()
    now = now.strftime("%d-%m-%Y %H:%M:%S %I")
    hDC.TextOut(10, Y, "Date: "+now)              
    Y += Y_distance
    id = str(uuid.uuid1())
    hDC.TextOut(10, Y, "Recipt #: "+id[0:5])              
    Y += Y_distance
    hDC.TextOut(10, Y, "Terminal #: 1234")              
    Y += Y_distance
    hDC.TextOut(10, Y, "Address: Dubai Investment Park First, Jabal Ali")              
    Y += Y_distance
    hDC.TextOut(10, Y, "-----------------------------------------")              
    Y += Y_distance
    #service_name = "etisalat | Prepaid"
    hDC.TextOut(10, Y, "Service: "+service_name)              
    Y += Y_distance
    hDC.TextOut(10, Y, "Entered Data:")              
    Y += Y_distance
    #contact_number = "0583009340"
    hDC.TextOut(10, Y, "Mobile number: "+contact_number)              
    Y += Y_distance
    amount_accepted = float(amount)
    hDC.TextOut(10, Y, "Accepted: AED "+str(amount_accepted))              
    Y += Y_distance
    
    Transacted = amount_accepted
    hDC.TextOut(10, Y, "Remaining: AED "+str(remaining))              
    Y += Y_distance
    hDC.TextOut(10, Y, "-----------------------------------------")              
    Y += Y_distance
    hDC.TextOut(10, Y, "Service provider's support # 090075601")              
    Y += Y_distance
    hDC.TextOut(10, Y, "NonStop Payments Support # 090075601")              
    Y += Y_distance
    hDC.TextOut(10, Y, "Dealer's support # 044448484")            
    Y += Y_distance
    hDC.TextOut(10, Y, "Whatsapp # 0568494189")            
    Y += Y_distance
    hDC.TextOut(10, Y, "Working hours: 09:00-22:00")              
    Y += Y_distance 
    hDC.TextOut(10, Y, "Keep the reciept until the payment is confirm!")                   
    Y += Y_distance
    hDC.EndPage()
    hDC.EndDoc() 
    trans = TRANSACTION()
    trans.pending_amount = remaining
    trans.total_payment = str(int(remaining)+int(amount))
    trans.phone = contact_number
    trans.plan = plan
    trans.service = service_name
    trans.receipt_id = id[0:5]
    return trans.toJson()



