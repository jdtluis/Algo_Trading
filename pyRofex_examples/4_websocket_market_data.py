# -*- coding: utf-8 -*-
"""
    Sample Module.

    Example of market data using websocket API.

    The code show how to initialize the connection,
    subscribe to market data for a list of valid and invalid instruments,
    and finally close the connection.

    Go to the official Documentation to check the API Responses.

    Steps:
    1-Initialize the environment
    2-Defines the handlers that will process the messages and exceptions.
    3-Initialize Websocket Connection with the handlers
    4-Subscribes to receive market data messages for a list of valid instruments
    5-Subscribes to an invalid instrument
    6-Wait 5 sec then close the connection
"""
import time

import pandas as pd
import pyRofex
import pandas
import configparser

config = configparser.SafeConfigParser()
found_config_file = config.read('config.cfg')
user = config['pyrofex'].get('user')
password = config['pyrofex'].get('password')
account = config['pyrofex'].get('account')
md = []
# 1-Initialize the environment
pyRofex.initialize(user=user,
                   password=password,
                   account=account,
                   environment=pyRofex.Environment.REMARKET)


# 2-Defines the handlers that will process the messages and exceptions.
def market_data_handler(message):
    print("Market Data Message Received: {0}".format(message))
    md.append(message['marketData'])


def error_handler(message):
    print("Error Message Received: {0}".format(message))


def exception_handler(e):
    print("Exception Occurred: {0}".format(e.msg))


# 3-Initialize Websocket Connection with the handlers
pyRofex.init_websocket_connection(market_data_handler=market_data_handler,
                                  error_handler=error_handler,
                                  exception_handler=exception_handler)


# 4-Subscribes to receive market data messages
instruments = ["PAMP/DIC22", "DLR/DIC22"]  # Instruments list to subscribe
entries = [pyRofex.MarketDataEntry.BIDS,
           pyRofex.MarketDataEntry.OFFERS,
           pyRofex.MarketDataEntry.LAST]

pyRofex.market_data_subscription(tickers=instruments,
                                 entries=entries)

# Subscribes to an Invalid Instrument (Error Message Handler should be call)
pyRofex.market_data_subscription(tickers=["InvalidInstrument"],
                                 entries=entries)


# Wait 5 sec then close the connection
time.sleep(5)
pyRofex.close_websocket_connection()

of = pd.DataFrame.from_dict(list(pd.DataFrame(md)['OF'].apply(lambda x: x[0]).values))
bi = pd.DataFrame.from_dict(list(pd.DataFrame(md)['BI'].apply(lambda x: x[0]).values))