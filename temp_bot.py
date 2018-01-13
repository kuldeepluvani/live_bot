import websocket
import json 
 
def on_message(ws, message):
    print("Message: " + message)
 
 
def on_error(ws, error):
    print("Error: " + error)
 
 
def on_close(ws, close):
    print("close")
 
 
if __name__ == "__main__":
 
    websocket.enableTrace(True)
    ws = websocket.create_connection("wss://streamer.cryptocompare.com")
    #ws = websocket.WebSocketApp("wss://streamer.cryptocompare.com",
    #                           on_message=on_message,
    #                           on_error=on_error,
    #                           on_close=on_close)


    ws.send(json.dumps({
        'SubAdd' : "[2~Poloniex~BTC~USD]")
    result = ws.recv()
    print result
