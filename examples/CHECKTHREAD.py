 
from datetime import datetime
import shortuuid
s = shortuuid.ShortUUID(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
import pymongo

class USER:
    def __init__(self) -> None:
        self.mac_address = None
        self.phone = None
        self.name = None
        self.ID = s.random(length=6)
    
    def toJson(self) -> dict:
        return self.__dict__

class TRANSACTION():
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


DBURL = "mongodb+srv://testUser:testUser@nv9-testing.9azuqdw.mongodb.net/?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(DBURL)
mydb = myclient["NV9-Testing"]
users = mydb["users"]
transactions = mydb["transactions"]
logs = mydb["log"]

tids = []
hits = 0
miss = 0
crashes = 0
try:
    transactions.delete_many({"service":{"$eq":"JWP"}})
        

except pymongo.errors.DuplicateKeyError as e:
    print(e)
    