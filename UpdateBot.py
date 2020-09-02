from py3cw.request import Py3CW
import argparse
import os
import pandas as pd
import MongoConnection
import requests


class UpdateBot:
    def __init__(self):
        self.db_object = MongoConnection.App_mongo_connect()
        # API key & Secret Key
        self.key = '3e45e0cb611845a19bc053f4752090704b20f1085c2d4951b4606b99d11db935'
        self.secret = 'a0dc20cb712001b1bad8eb82d1e453b5b70042897d417fc4d3ba84efb734190d30759bd61' \
                      'c69df14032ddb1ee3eafbb923e95683c4114e65a35fee54e0420d2ad5902a5432c266273d7f7cd' \
                      'f3e07285b8ecdf5e431679b1c0a7a8f76b51c5b77a20aaac7'
        # py3wc Object
        self.py3cw = Py3CW(self.key,self.secret)
        # Argument input_file
        parser = argparse.ArgumentParser()
        parser.add_argument('--input_file', type=str,
                            default='', help='Default - ""')
        args = vars(parser.parse_args())

        print("Input arguments:")
        print(args)
        print("*"*40)

        self.input_file = args['input_file']
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.bot_table_path = os.path.join(self.abs_path, "Bot_tables")
        self.file = os.path.join(self.bot_table_path,self.input_file)

    def bot_information(self):
        """
            this methods return the bots to be updated with new pairs.
        :return: bots_with_new_pairs
        """
        self.bots_with_new_pairs = []
        # Checking Bot_table exist in Bot_tables folder
        if os.path.isfile(self.file):
            self.bot_table = pd.read_csv(self.file)
            print(self.bot_table.head())
            print("*"*40)
            for bot in self.bot_table.index:
                bot = self.bot_table.loc[bot]
                if not pd.isnull(bot['New_pairs']):
                    self.bots_with_new_pairs.append({"name" : bot['Bot_name'],
                                                    "id" :  bot['Bot_id'], "new_pairs" :  bot['New_pairs']})
        return self.bots_with_new_pairs

    def update_bot(self):
        bot_ids_with_new_pairs = []
        for bot in self.bots_with_new_pairs:
            bot_ids_with_new_pairs.append(bot['id'])
        try:
            self.bots_information_from_db = self.db_object.get_bot_data(bot_ids_with_new_pairs)
        except Exception as e:
            print("Bot Information not recived from Database, error statement : "+ str(e))
        else:
            print("Bot Information Loaded from Database.")
            print("*"*40)
        # Replacing pairs in Bot with New_pairs
        bots_to_be_updated = []
        for bot_db in self.bots_information_from_db:
            bots_to_be_updated.append(bot_db['name'])
            for bot_new_pairs in self.bots_with_new_pairs:
                if bot_db['id'] == bot_new_pairs['id']:
                    bot_db['pairs'] = bot_new_pairs['new_pairs'].split(",")

        print("Bots to be updated are:")
        print(bots_to_be_updated)
        print("*"*40)
        conform = input("Are you sure to update above mentioned bots? (y/n)")
        if conform == 'y' or conform == "Y":
            for bot in self.bots_information_from_db:
                del bot['leverage_custom_value']
                del bot['bots_status']
                del bot['max_active_deals']
                #del bot['finished_deals_profit_local']
                # Updating DB



                error, data = self.py3cw.request(
                    entity='bots',
                    action='update',
                    action_id= str(bot['id']),
                    payload=bot
                )
                if error:
                    print(error)
                else:
                    print(str(bot['name']) + "Bot Updated Successfully.")
        else:
            print("Terminated!")
            exit()



def update_bot():
    Bot_obj = UpdateBot()
    Bot_obj.bot_information()
    Bot_obj.update_bot()

if __name__ == '__main__':
    update_bot()

