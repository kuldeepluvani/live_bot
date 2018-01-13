import requests
import json
from socketIO_client import SocketIO
import socket

fsym = "BTC"
tsym = "USD"

url = "https://min-api.cryptocompare.com/data/subs?fsym=" + fsym + "&tsyms=" + tsym
stream_url = "wss://streamer.cryptocompare.com/"



page = requests.get(url)
data = page.json()

socket = io(stream_url)
SocketIO.emit('SubAdd',{subs: data['USD']['CURRENT'][1]})
