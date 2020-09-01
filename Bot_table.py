import MongoConnection
import pandas as pd
import os
from datetime import datetime

class Bot_table:
    def __init__(self):
        db_object = MongoConnection.App_mongo_connect()
        self.bot_table_data = db_object.get_update_table()
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.bot_table_path = os.path.join(self.abs_path,"Bot_tables")
        print("*" * 40)

    def generate_bot_table(self):
        print("Generating Bot table Please wait....")
        output = pd.DataFrame(columns=['Bot_name', 'Bot_id', "Current_pairs"])
        for document in self.bot_table_data:
            row = pd.Series([document['name'], document['id'], ",".join(document['pairs'])],
                            index=['Bot_name', 'Bot_id', "Current_pairs"])
            output = output.append(row, ignore_index=True)
        print(output.head())
        print("Done")
        print("*" * 40)
        print("Exporting File...")
        file_name = "Update_table" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".csv"
        output.to_csv(os.path.join(self.bot_table_path,file_name), index=False)
        print("Done")


Db_connect = Bot_table()
Db_connect.generate_bot_table()
