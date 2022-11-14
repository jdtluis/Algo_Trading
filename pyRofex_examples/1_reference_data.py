# -*- coding: utf-8 -*-
"""
    Sample Module.

    Example for reference data using the library.

    The code show how to work with segments and instrument data using pyRofex.

    Go to the official Documentation to check the API Responses.

    Steps:
    1-Initialize the environment
    2-Get all available segments and print all segment ids
    3-Get a list of all instruments and then count the number of instruments return
    4-Get a detailed list of the instruments and then check the Low Limit Price for the first instrument return
"""
import pyRofex
import configparser

config = configparser.SafeConfigParser()
found_config_file = config.read('config.cfg')
user = config['pyrofex'].get('user')
password = config['pyrofex'].get('password')
account = config['pyrofex'].get('account')

# 1-Initialize the environment
pyRofex.initialize(user=user,
                   password=password,
                   account=account,
                   environment=pyRofex.Environment.REMARKET)

# 2-Get all available segments and print all segment ids
segments = pyRofex.get_segments()
for segment in segments['segments']:
    print("Segment ID: {0}".format(segment['marketSegmentId']))

# Get a list of all instruments and then count the number of instruments return
instruments = pyRofex.get_all_instruments()
print("Number of Instruments: {0}".format(len(instruments['instruments'])))

# 4-Get a detailed list of the instruments and then check the Low Limit Price for the first instrument return
detailed = pyRofex.get_detailed_instruments()
print("Low Limit Price for {0} is {1}.".format(detailed['instruments'][0]['instrumentId']['symbol'],
                                               detailed['instruments'][0]['lowLimitPrice']))

detal_instruments = pyRofex.get_instrument_details('ORO/NOV22',pyRofex.Market.ROFEX,pyRofex.Environment.REMARKET)