from pymongo import MongoClient
import pandas as pd
import json

class App_mongo_connect:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://dbReader:kriE0s9iWeYnRGD1@cluster0.8bri5.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client.ccMain

    def get_update_table(self):
        threecommasbots_db= self.db.threeCommasBots.find({"account_id": 27977007})
        if (threecommasbots_db == None):
            print("FAILED: loading data report from ")
        else:
            print("Data loaded successfully.")
            return list(threecommasbots_db)
    def get_bot_data(self,bot_ids_with_new_pairs):
        active_bot_to_update = []
        active_bots = self.db.threeCommasBots.find({"account_id": 27977007}, {'_id': False})
        active_bots = list(active_bots)
        for bot in active_bots:
            if bot['id'] in bot_ids_with_new_pairs:
                active_bot_to_update.append(bot)

        return active_bot_to_update


    def __del__(self):
        self.client.close()