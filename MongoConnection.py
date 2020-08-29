from pymongo import MongoClient
from pprint import pprint

class App_mongo_connect:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://dbReader:kriE0s9iWeYnRGD1@cluster0.8bri5.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client.ccMain

    def get_update_table(self):
        threecommasbots_db= self.db.threeCommasBots.find({"name":"AUTO TEST 1"})
        if (threecommasbots_db == None):
            print("FAILED: Loading data report from ")
        else:
            print("Data Loaded Successfully.")
            return list(threecommasbots_db)[0]
    def __del__(self):
        self.client.close()
