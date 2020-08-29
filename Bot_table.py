import MongoConnection
import pandas as pd
from datetime import datetime

class Bot_table:
    def __init__(self):
        db_object = MongoConnection.App_mongo_connect()
        self.bot_table_data = db_object.get_update_table()
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
        output.to_csv("Update_table" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".csv", index=False)
        print("Done")


Db_connect = Bot_table()
Db_connect.generate_bot_table()
