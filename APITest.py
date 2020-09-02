import requests
import json
x = requests.post("http://142.93.42.209:5001/3commas/bots/1390329",{"pairs":["BTC_ZRX","BTC_ADA","BTC_ADX","BTC_AE"]})
print(x.text)