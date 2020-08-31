from py3cw.request import Py3CW

p3cw = Py3CW(key='3e45e0cb611845a19bc053f4752090704b20f1085c2d4951b4606b99d11db935',
             secret='a0dc20cb712001b1bad8eb82d1e453b5b70042897d417fc4d3ba84efb734190d30759bd61c69df14032ddb1ee3eafbb923e95683c4114e65a35fee54e0420d2ad5902a5432c266273d7f7cdf3e07285b8ecdf5e431679b1c0a7a8f76b51c5b77a20aaac7')

# Data from the bot

error, data_from_bot = p3cw.request(
    entity='bots',
    action=''
)
# Checking if no error
if not error:
    print(data_from_bot)
# Udating Some values into the bot
error, data = p3cw.request(
    entity='bots',
    action='update',
    action_id='1390329',
    payload={'name': 'AUTO TEST 1',
             'pairs': ['BTC_ADA', 'BTC_ADX', 'BTC_AE', 'BTC_AGI', 'BTC_AION', 'BTC_ALGO', 'BTC_AMB', 'BTC_ANKR'],
             'base_order_volume': '0.0002',
             'take_profit': '2.5',
             'safety_order_volume': '0.0002',
             'martingale_volume_coefficient': '2',
             'martingale_step_coefficient': '2',
             'max_safety_orders': '2',
             'active_safety_orders_count': '2',
             'safety_order_step_percentage': '2',
             'take_profit_type': 'total',
             'stop_loss_percentage' : 10,
             'cooldown' : '5',
             'strategy_list': [{'options': {'time': '1m', 'type': 'buy_or_strong_buy'},
                                'strategy': 'trading_view'}, {'options': {'time': '1h', 'points': '39'},
                                                              'strategy': 'rsi'}]
             }
)
print(data)
