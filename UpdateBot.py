from py3cw.request import Py3CW
import argparse
import os
import numpy as np
import pandas as pd
import MongoConnection
import json


class UpdateBot:
    def __init__(self):
        self.db_object = MongoConnection.App_mongo_connect()
        self.key = '3e45e0cb611845a19bc053f4752090704b20f1085c2d4951b4606b99d11db935'
        self.secret = 'a0dc20cb712001b1bad8eb82d1e453b5b70042897d417fc4d3ba84efb734190d30759bd61' \
                      'c69df14032ddb1ee3eafbb923e95683c4114e65a35fee54e0420d2ad5902a5432c266273d7f7cd' \
                      'f3e07285b8ecdf5e431679b1c0a7a8f76b51c5b77a20aaac7'
        self.py3cw = Py3CW(self.key,self.secret)

        parser = argparse.ArgumentParser()
        parser.add_argument('--input_file', type=str,
                            default='', help='Default - ""')
        args = vars(parser.parse_args())

        print("Input arguments:")
        print(args)

        self.input_file = args['input_file']
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.bot_table_path = os.path.join(self.abs_path, "Bot_tables")
        self.file = os.path.join(self.bot_table_path,self.input_file)

    def bot_information(self):
        self.bot_with_new_pairs = []
        if os.path.isfile(self.file):
            self.bot_table = pd.read_csv(self.file)
            print(self.bot_table)
            for bot in self.bot_table.index:
                bot = self.bot_table.loc[bot]
                if not pd.isnull(bot['New_pairs']):
                    self.bot_with_new_pairs.append({"name" : bot['Bot_name'],
                                                    "id" :  bot['Bot_id'], "new_pairs" :  bot['New_pairs']})
        return self.bot_with_new_pairs

    def update_bot(self):

        self.bot_information_from_db = self.db_object.get_bot_data(self.bot_with_new_pairs)
        print(self.bot_information_from_db)
        for bot_db in self.bot_information_from_db:
            for bot_new_pairs in self.bot_with_new_pairs:
                if bot_db['id'] == bot_new_pairs['id']:
                    bot_db['pairs'] = bot_new_pairs['new_pairs'].split(",")
        print(self.bot_information_from_db)
        global error
        for bot in self.bot_information_from_db:
            print(bot)
            # converting values to string
            for key,value in list(bot.items()):
                if isinstance(value,int):
                    bot[key] = str(value)
            error, data = self.py3cw.request(
                entity='bots',
                action='update',
                action_id= str(bot['id']),
                payload=bot
            )
            if error:
                print(error)




Bot_obj = UpdateBot()
Bot_obj.bot_information()
Bot_obj.update_bot()


