from pymongo import MongoClient
import pandas as pd
import json

class App_mongo_connect:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://dbReader:kriE0s9iWeYnRGD1@cluster0.8bri5.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client.ccMain

    def get_update_table(self):
        threecommasbots_db= self.db.threeCommasBots.find({"is_enabled": True})
        if (threecommasbots_db == None):
            print("FAILED: Loading data report from ")
        else:
            print("Data Loaded Successfully.")
            return list(threecommasbots_db)
    def get_bot_data(self,bot_with_new_pairs):
        print(bot_with_new_pairs)
        bot_data = []
        id = []
        for bot in bot_with_new_pairs:
            id.append(bot['id'])
        print(id)
        active_bot_data = self.db.threeCommasBots.find({"is_enabled": True})
        active_bot_data = list(active_bot_data)
        for bot in active_bot_data:
            if bot['id'] in id:
                bot_data.append(bot)

        return bot_data


    def __del__(self):
        self.client.close()