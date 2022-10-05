import requests

import configparser

config = configparser.SafeConfigParser()
found_config_file = config.read('pyRofex_examples\config.cfg')
user = config['pyrofex'].get('user')
password = config['pyrofex'].get('password')

headers = \
    {'X-Username': user,
    'X-Password': password}
response = requests.post("https://api.remarkets.primary.com.ar/" + "auth/getToken",
                         headers=headers,)

token = response.headers['X-Auth-Token']



import websocket, rel

addr = "wss://api.gemini.com/v1/marketdata/%s"
for symbol in ["BTCUSD", "ETHUSD", "ETHBTC"]:
    ws = websocket.WebSocketApp(addr % (symbol,), on_message=lambda w, m : print(m))
    ws.run_forever(dispatcher=rel)

rel.signal(2, rel.abort)  # Keyboard Interrupt
rel.dispatch()

