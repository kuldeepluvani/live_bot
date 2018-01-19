import json
from websocket import create_connection
from datetime import datetime
import argparse
import sys

instance = 3

parser = argparse.ArgumentParser()
parser.add_argument('-l','--log', help='Log to some file?', default='n')
args = parser.parse_args()

if args.log == 'n' or args.log == 'N':
    pass
else:
    try:
        sys.stdout = open(args.log, 'a')
    except:
        try:
            sys.stdout = open(args.log, 'w')
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception, e:
            print "Failed to open a file:", args.log
       
print "\n\n--------------------------------------------"
print "Bot started at:", datetime.now(), "\n"
    
def moving_average(a, N):
    cumsum = [0]
    moving_avg = [0]
    
    for i, x in enumerate (a,1):
        cumsum.append(cumsum[i-1] + x)
        if i>= N:
            moving = (cumsum[i] - cumsum[i-N])/N
            moving_avg.append(moving)
    return moving_avg[-1]

def trade(buy_flag, coin_price, trading_account_balance, coin_balance, taka):
    if buy:
        buying_amount = trading_account_balance*taka/trading_account_balance
        coin_balance += buying_amount/coin_price
        trading_account_balance -= buying_amount
    else:
        selling_coin = coin_balance*taka/coin_balance
        coin_balance -= selling_coin
        trading_account_balance += selling_coin*coin_price

    return coin_balance, trading_account_balance

webs = create_connection('wss://api.bitfinex.com/ws')


webs.send(json.dumps({
                'event':'subscribe',
                'channel': 'trades',
                'pair':"BTCUSD"}))
for k in range(3):
    response = webs.recv()


pending = []
current_price = []
sold, buy = 0,0
total_trade_sold, total_trade_bought = 0, 0
previous_avg = 0
count = 0
initial_assets = 0
coin_balance = 10
trading_account_balance = 1000000
neg_checker = 0
force_flag_set = 0
while True:
    response = webs.recv()
    response = json.loads(response)
    if response[1] == 'hb':
        pass
    elif response[1] == 'te':
        pending.append(int(response[2].strip('-BTCUSD')))
    elif response[1] == 'tu':
        if int(response[2].strip('-BTCUSD')) in pending:
            pending.remove(int(response[2].strip('-BTCUSD')))

        current_price.append(float(response[-2]))
        
        if len(current_price) >= instance:
            previous_avg = float(moving_average(current_price, instance))
            if initial_assets == 0:
                initial_assets = coin_balance * current_price[0] + trading_account_balance
            current_price = current_price[1:]
            count += 1
        #print ("Current price",float(response[-2]), "Average price", previous_avg)
        if response[-1] < 0:
            sold += 1
            total_trade_sold += abs(int(response[-1]))
        if response[-1] > 0:
            buy += 1
            total_trade_bought += abs(int(response[-1]))

        if count == instance:
            taka = ((response[-2]-previous_avg)/response[-2])*100
            if taka>0:
                temp_buyflag = False
                action = "SELL"
            else:
                temp_buyflag = True
                action = "BUY "
            count = 0
            '''if total_trade_sold >= total_trade_bought:
                buy_flag = True
                action = "BUY"
            else:
                buy_flag = False
                action = "SELL "'''

            total_balance = coin_balance*response[-2] + trading_account_balance
            percentage_change = ((total_balance-initial_assets)/total_balance)*100
            
            if abs(percentage_change) > 0.001:
                force_flag_set = 0
                if action == "SELL":
                    action_1 = "BUY "
                else:
                    action_1 = "SELL"
                print "Force flag set"
                '''#neg_checker += 1
                if neg_checker >= 5:
                    #force_flag = !temp_buyflag
                    force_flag_set = 1
                    if action == "SELL":
                        action_1 = "BUY "
                    else:
                        action_1 = "SELL"
                    print "Force flag set"
                    neg_checker = 0'''
            else:
                neg_checker = 0

            #print previous_avg, response[-2], "CHANGE", taka
            if action:
                #taka = 50
                sign = action
                if force_flag_set == 1:
                    force_flag_set = 0
                    sign = action_1
                    print "IT wants to", action,
                    temp_buyflag = not(temp_buyflag)
                    print " IT will do ", action_1
                    taka = 90
                coin_balance, trading_account_balance = trade(temp_buyflag, response[-2], trading_account_balance, coin_balance, taka)
            total_balance = coin_balance*response[-2] + trading_account_balance
            percentage_change = ((total_balance-initial_assets)/total_balance)*100

            
            
            print datetime.now(),"STRATED WITH",initial_assets, sign, "MONEY I HAVE", total_balance, percentage_change,"%"
            total_trade_sold = 0
            total_trade_bought = 0

            
