from datetime import datetime
import shortuuid
s = shortuuid.ShortUUID(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

class VOUCHER:
    def __init__(self) -> None:
        self.TID = s.random(length=15)
        self.receipt_id = None
        self.pin = None
        now = datetime.now()
        dt_time = now.strftime("%H:%M:%S")
        dt_date = now.strftime("%d/%m/%Y")
        self.time = dt_time
        self.date = dt_date
        self.service = None
        self.phone = None
        self.plan = 0
        self.payment = 0
    
    def toJson(self) -> dict:
        return self.__dict__
class USER:
    def __init__(self) -> None:
        self.mac_address = None
        self.phone = None
        self.name = None
        self.ID = s.random(length=6)
    
    def toJson(self) -> dict:
        return self.__dict__
class PLAN:
    def __init__(self) -> None:
        self.profile = None
        self.validity = None
        self.price  = None

    def toJson(self) -> dict:
        return self.__dict__

        
class TRANSACTION:
    def __init__(self) -> None:
        self.TID = s.random(length=15)
        self.receipt_id = None
        now = datetime.now()
        dt_time = now.strftime("%H:%M:%S")
        dt_date = now.strftime("%d/%m/%Y")
        self.time = dt_time
        self.date = dt_date
        self.service = None
        self.phone = None
        self.pending_amount = 0
        self.plan = None
        self.total_payment = 0

    def toJson(self)-> dict:
        return self.__dict__

class LOG:
    def __init__(self) -> None:
        now = datetime.now()
        dt_time = now.strftime("%H:%M:%S")
        dt_date = now.strftime("%d/%m/%Y")
        self.time = dt_time
        self.date = dt_date
        self.log = None
    
    def toJson(self) -> dict:
        return self.__dict__

