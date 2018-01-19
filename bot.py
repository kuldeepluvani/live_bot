import json
import pandas 
import requests
from websocket import create_connection


ws = create_connection('wss://api.bitfinex.com/ws')

#pair fetching
url = "https://api.bitfinex.com/v1/symbols"
coinpair = requests.request("GET", url)

cp = coinpair.text[0]

ws.send(json.dumps({
    "event": "subscribe",
    "channel": "trades",
    "pair": "ETHUSD",
    "prec": "P0"
}))



def moving_average(a, N):
    cumsum = [0]
    moving_avg = [0]
    
    for i, x in enumerate (a,1):
        cumsum.append(cumsum[i-1] + x)
        if i>= N:
            moving = (cumsum[i] - cumsum[i-N])/N
            moving_avg.append(moving)
    return moving_avg[-1]


pending = []
data = []
X = True
i = 0
k = 0
SOLD = 0
BUY = 0
total_trade_sell = 0.000000
total_trade_buy = 0.000000
flg = False
while X:
    result = ws.recv()
    result = json.loads(result)
    i += 1
    if i > 3:
        if result[1] == 'te':
            pending.append(result[2][0])
        elif result[1] == 'hb':
            pass
        elif result[1] == 'tu':
            if result[2][0] in pending:
                pending.remove(result[2][0])



            if k == 0:
                current_price = []
                if flg:
                     previous_avg = current_avg
                else:
                    previous_avg = 0
                    flg = True
            
            current_price.append(result[2][3])

            
            if result[2][2] < 0:
                SOLD += 1
                k += 1
                total_trade_sell += abs(result[2][2])
                #print ("BTC SOLD in ", result[2][3], "AMOUNT", abs(result[2][2]), "BUY:", BUY,"SOLD:", SOLD)
            elif result[2][2] >0:
                BUY += 1
                k += 1
                total_trade_buy += abs(result[2][2])
                #print ("BTC BUY in ", result[2][3], "AMOUNT", abs(result[2][2]),"BUY:", BUY,"SOLD:", SOLD)

            if k == 10:
                final_price = result[2][3]
                print ("Total_Trade_sell", round(total_trade_sell,6), "Total_Trade_BUY", round(total_trade_buy,6)),
                total_trade_sell = 0.000000
                total_trade_buy = 0.000000
                current_avg = sum(current_price)/len(current_price)
                current_price = []
                print "current_avg", current_avg, "previous_avg", previous_avg,
                if current_avg - previous_avg >0:
                    print "UP"
                else:
                    print "DOWN"
                k = 0
            
        data.append(result)
        #print ("Received '%s'" % result)
    
ws.close()

'''

trades = client.get_recent_trades(symbol='BNBBTC')


'''
