from py3cw.request import Py3CW
p3cw = Py3CW(key='3e45e0cb611845a19bc053f4752090704b20f1085c2d4951b4606b99d11db935',
             secret='a0dc20cb712001b1bad8eb82d1e453b5b70042897d417fc4d3ba84efb734190d30759bd61c69df14032ddb1ee3eafbb923e95683c4114e65a35fee54e0420d2ad5902a5432c266273d7f7cdf3e07285b8ecdf5e431679b1c0a7a8f76b51c5b77a20aaac7')

# Data from the bot

error, data_from_bot = p3cw.request(
    entity='bots',
    action = ''
)
# Checking if no error
if not error:
    print(data_from_bot)

# Udating Some values into the bot
error, data = p3cw.request(
    entity='bots',
    action = 'update',
    action_id='1390329',
    payload = {
        "max_active_deals" : 10,
        "min_price" : 50
    }
)
print(data)