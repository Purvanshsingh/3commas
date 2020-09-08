import MongoConnection
import pandas as pd
import os
from datetime import datetime

class Bots_table:
    def __init__(self):
        db_object = MongoConnection.App_mongo_connect()
        self.bots_table_data = db_object.get_update_table()
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.bots_table_path = os.path.join(self.abs_path,"Bot_tables")
        self.mandatory_columns = ['Bot_name', 'Bot_id', "Current_pairs", "base_order_volume", "take_profit",
                                       "safety_order_volume", "martingale_volume_coefficient",
                                       "martingale_step_coefficient","max_safety_orders", "active_safety_orders_count",
                                       "safety_order_step_percentage","take_profit_type", "strategy_list",
                                       "stop_loss_percentage", "cooldown", "max_active_deals"]
        print("*" * 40)

    def generate_bots_table(self):
        print("Generating bots table please wait...")
        output = pd.DataFrame(columns=self.mandatory_columns)

        for document in self.bots_table_data:
            row = pd.Series([document['name'], document['id'], ",".join(document['pairs']),
                             document["base_order_volume"], document["take_profit"],document["safety_order_volume"],
                             document["take_profit"], document["martingale_volume_coefficient"],
                             document["martingale_step_coefficient"], document["max_safety_orders"],
                             document["active_safety_orders_count"],document["safety_order_step_percentage"],
                             document["take_profit_type"], document["strategy_list"],document["stop_loss_percentage"],
                             document["cooldown"], document["max_active_deals"]], index=self.mandatory_columns)
            output = output.append(row, ignore_index=True)
        output['New_pairs'] = None
        print(output.head())
        print("Done")
        print("*" * 40)
        print("Exporting file...")
        file_name = "Update_table" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".csv"
        output.to_csv(os.path.join(self.bots_table_path,file_name), index=False)
        print("Done")


Db_connect = Bots_table()
Db_connect.generate_bots_table()
