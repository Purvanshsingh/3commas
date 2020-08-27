from pymongo import MongoClient
from functools import reduce
from pprint import pprint
from datetime import datetime, timezone, timedelta


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

    def get_report_by_time(self, interval, created_for_time):
        db_result = self.db.market_TA_reports_binance.find_one(
            {"interval": interval, "created_for_time": created_for_time})
        if(db_result == None):
            print("FAILED: Loading data report from "+str(created_for_time))
            return False

        result = dict(db_result)
        print("SUCCESS: Loading data report from " +
              result['hr_created_for_time'] + "("+str(created_for_time)+")")
        return result

    def get_last_200(self, interval, input_datetime):
        '''
            This method will be used for get last 200 points from database starting from last_time.
        '''
        interval_minutes = 60
        if(interval == '1h'):
            interval_minutes = 60
        if(interval == '1m'):
            interval_minutes = 1
        if(interval == '4h'):
            interval_minutes = 60 * 4

        date_from = input_datetime.timestamp() * 1000 - 200 * 1000 * 60 * interval_minutes
        date_to = input_datetime.timestamp() * 1000 - 1 * 1000 * 60 * interval_minutes

        
        #print("Date from "+input_datetime.strftime("%Y-%m-%d %H:%M:%S%z")+" Date to "+datetime.fromtimestamp(date_to / 1000).strftime("%Y-%m-%d %H:%M:%S%z"))

        pipeline = [
            # setting exchange and interval // 'pair': 'ADABTC',
            {"$match": {"interval": interval, "exch_name": 'Binance'}},
            {
                "$match":

                {
                    "$and": [
                        {"open_time": {"$gte": date_from}},
                        {"open_time": {"$lte": date_to}}
                    ]
                }

            },
            {"$sort": {"open_time": -1}},
            {
                "$group": {
                    "_id": '$pair',
                    "prices": {"$push": {  # getting all the data we need
                        "open_time": '$open_time',
                        "close_time": '$close_time',
                        "exch_volume": '$exch_volume',
                        "price_low": {"$toDouble": '$price_low'},
                        "price_high": {"$toDouble": '$price_high'},
                        "price_open": {"$toDouble": '$price_open'},
                        "price_close": {"$toDouble": '$price_close'},
                        "to_ccy": "$to_ccy",

                    }}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "pair": '$_id',
                    "prices_array": {"$slice": [{"$reverseArray": '$prices'}, -200]},
                }
            },
            {"$sort": {"pair": 1}}
        ]

        pairs_dictionary = list(self.db.market_data_v1.aggregate(pipeline))

        def convert_to_csv(pair_dict):
            pricesArray = pair_dict.get("prices_array")

            def add_pair(price_dict):
                return {
                    "pair": pair_dict.get('pair'),
                    "open_time": price_dict.get("open_time"),
                    "to_ccy": price_dict.get("to_ccy"),
                    "close_time": price_dict.get("close_time"),
                    "exch_volume": price_dict.get("exch_volume"),
                    "price_low": price_dict.get("price_low"),
                    "price_high": price_dict.get("price_high"),
                    "price_open": price_dict.get("price_open"),
                    "price_close": price_dict.get("price_close")
                }
            return list(map(add_pair, pricesArray))

        list_of_lists = list(map(convert_to_csv, pairs_dictionary))

        # print(list_of_lists)

        def merge_lists(first, second):
            return first + second

        csv_format_result = reduce(merge_lists, list_of_lists)
        return csv_format_result

        # print(csv_format_result)

    def save_results_to_db(self, interval, data, input_datetime, alerts={}, malformed_currencies={}):
        market_TA_reports_binance = self.db.market_TA_reports_binance
        hr_created_for_time = input_datetime.strftime("%Y-%m-%d %H:%M:%S%z")
        trading_view_time = (input_datetime - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S%z")

        created_for_time_ms = input_datetime.timestamp() * 1000

        insert_data = {
            "created_for_time": created_for_time_ms,
            "hr_created_for_time": hr_created_for_time,
            "trading_view_time": trading_view_time,
            "interval": interval,
            "inserted": datetime.now(timezone.utc),  # utc by default
            "data": data,
            "soft_errors": [],
            "hard_errors": [],
            "alerts": alerts,
            "malformed_currencies": malformed_currencies
        }
        # print(insert_data)
        '''
        test_data = {
            "interval": interval,
            "inserted": datetime.now().strftime("%d_%m_%Y_%H_%M_%S"),
            "data": {},
            "soft_errors": [],
            "hard_errors": [],
        }
        '''
        market_TA_reports_binance.update_one({'created_for_time': created_for_time_ms, "interval": interval, },
                                             {"$set": insert_data}, upsert=True)
        print("Sent to DB")
        return True

    def __del__(self):
        self.client.close()
