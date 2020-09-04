from py3cw.request import Py3CW
import argparse
import os
import pandas as pd
import MongoConnection
import requests


class UpdateBots:
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
        parser.add_argument('--force', type=bool,
                            default=False, help='Default - False')
        args = vars(parser.parse_args())

        print("Input arguments:")
        print(args)
        print("*"*40)

        self.input_file = args['input_file']
        self.force = args['force']
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.bots_table_path = os.path.join(self.abs_path, "Bot_tables")
        self.file = os.path.join(self.bots_table_path,self.input_file)

    def bots_information(self):
        """
            This methods return the bots to be updated with new pairs.
        :return: bots_with_new_pairs
        """
        self.bots_with_new_pairs = []
        # Checking Bot_table exist in Bot_tables folder
        if os.path.isfile(self.file):
            self.bots_table = pd.read_csv(self.file)
            print(self.bots_table.head())
            print("*"*40)
            for bot in self.bots_table.index:
                bot = self.bots_table.loc[bot]
                if not pd.isnull(bot['New_pairs']):
                    self.bots_with_new_pairs.append({"name" : bot['Bot_name'],
                                                    "id" :  bot['Bot_id'], "new_pairs" :  bot['New_pairs']})
        return self.bots_with_new_pairs

    def update_bots(self):
        bot_ids_with_new_pairs = []
        for bot in self.bots_with_new_pairs:
            bot_ids_with_new_pairs.append(bot['id'])
        try:
            self.bots_information_from_db = self.db_object.get_bot_data(bot_ids_with_new_pairs)
        except Exception as e:
            print("Bot information not received from database, error statement : "+ str(e))
        else:
            print("Bots information received from database")
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
        if self.force == False:
            conform = input("Are you sure to update mentioned above bots? (y/n)")
        else:
            print("Forcefully updating bots...")
            conform = 'y'
        if conform == 'y' or conform == "Y":
            mandatory_arguments = ["name", "pairs", "base_order_volume", "take_profit", "safety_order_volume",
                                   "take_profit", "martingale_volume_coefficient", "martingale_step_coefficient",
                                   "max_safety_orders", "active_safety_orders_count", "safety_order_step_percentage",
                                   "take_profit_type", "strategy_list", "id","stop_loss_percentage", "cooldown"]
            for bot in self.bots_information_from_db:
                # only passing mandatory parameter.
                for key in list(bot.keys()):
                    if key not in mandatory_arguments:
                        del bot[key]
                # If any argument from mandatory_arguments is None then dropping them.
                for key in mandatory_arguments:
                    if bot[key] is None:
                        del bot[key]
                # Updating DataBase
                update = requests.post("http://142.93.42.209:5001/3commas/bots/"+str(bot["id"]),
                                       {"pairs":bot['pairs']})
                # Updating bot
                error, data = self.py3cw.request(
                    entity='bots',
                    action='update',
                    action_id= str(bot["id"]),
                    payload=bot
                )
                # Checking for errors in Updating Bot
                if error:
                    print(error)
                # Checking for errors in Updating DataBase
                if update.status_code != requests.codes.ok:
                    print(update.text)
                if error is None and update.status_code is requests.codes.ok :
                    print(str(bot['name']) + " Bot in the API and in the database was updated successfully.")
        else:
            print("Terminated!")
            exit()



def update_bots():
    Bots_obj = UpdateBots()
    Bots_obj.bots_information()
    Bots_obj.update_bots()

if __name__ == '__main__':
    update_bots()

