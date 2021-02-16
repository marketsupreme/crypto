#!/usr/bin/env python
# coding: utf-8

import requests
import json
import time

file = open('README.md', 'w')
 
file.write('Welcome to the Meyers Crypto Portfolio Value tool. \n')
file.write('Please see below for our valuation.\n\n\n')

prices = requests.get('https://api.nomics.com/v1/currencies/ticker?key=ea386addbac03f4bb67ceb1f333a8d0a&ids=BTC,ETH&interval=1d&convert=USD&per-page=100&page=1')

data = prices.json()

bit_price = float(data[0]['price'])
eth_price = float(data[1]['price'])

file.write(f'Current price of BTC is ${bit_price} and current price of ETH is ${eth_price}\n')

e = requests.get('https://api.ethplorer.io/getAddressInfo/0xed8b4b3ba4fd5a175613859cab6ab8f010276a3a?apiKey=freekey')
data = e.json()

eth_holdings = float(data['ETH']['balance'])

b = requests.get('https://blockchain.info/balance?active=16MuqwYTRT1qTFmwF5WsgfsrA9rE3UmPQN')
data = b.json()

bit_holdings1 = data['16MuqwYTRT1qTFmwF5WsgfsrA9rE3UmPQN']['final_balance']
bit_holdings = 0.98

file.write(f'Current holdings of BTC is {bit_holdings}BTC and current holdings of ETH is {eth_holdings}ETH \n\n')


# In[40]:


eth = eth_holdings*eth_price
bit = bit_holdings*bit_price

value = eth+bit

file.write(f'Current Portfoio Value is ${value}\n')
time.sleep(3)






