import requests
import json

url = "https://min-api.cryptocompare.com/data/histohour?fsym=ETH&tsym=USD&limit=200&aggregate=3&e=Kraken"


response = requests.request("GET", url)
response = json.loads(response.text)


def trade(flag, coin_price, trading_account_balance, coin_balance, taka):
    if flag == 'buy':
        buying_amount = trading_account_balance*taka/trading_account_balance
        coin_balance += buying_amount/coin_price
        trading_account_balance -= buying_amount
    else:
        selling_coin = coin_balance*taka/coin_balance
        coin_balance -= selling_coin
        trading_account_balance += selling_coin*coin_price

    return coin_balance, trading_account_balance


data = response["Data"]
