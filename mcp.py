#!/usr/bin/env python
# coding: utf-8

from requests import get
import json
import time as t
from datetime import date, datetime
import pandas as pd
from openpyxl import load_workbook

def getValue():

    prices = get('https://api.nomics.com/v1/currencies/ticker?key=ea386addbac03f4bb67ceb1f333a8d0a&ids=BTC,ETH&interval=1d&convert=USD&per-page=100&page=1')
    data = prices.json()

    bit_price = round(float(data[0]['price']),2)
    eth_price = round(float(data[1]['price']),2)

    e = get('https://api.ethplorer.io/getAddressInfo/0xed8b4b3ba4fd5a175613859cab6ab8f010276a3a?apiKey=freekey')
    data = e.json()

    eth_holdings = data['ETH']['balance']

    # b = get('https://blockchain.info/balance?active=16MuqwYTRT1qTFmwF5WsgfsrA9rE3UmPQN')
    # data = b.json()

    # bit_holdings1 = data['16MuqwYTRT1qTFmwF5WsgfsrA9rE3UmPQN']['final_balance']
    bit_holdings = 1.06

    eth_value = eth_holdings*eth_price
    bit_value = bit_holdings*bit_price

    return [bit_price, bit_value, bit_holdings, eth_price, eth_value, eth_holdings]

def main():

    file = open('README.md', 'w')
    today = date.today().strftime("%m/%d/%y")
    time = datetime.now().strftime("%H:%M:%S")

    coin_list = getValue()

    vals = round(coin_list[1]+coin_list[4],2)

    file.write(f'\t\t{today} @ {time} \n\n\n\n')
    file.write(f'\t\tValue: ${vals}\n\n\n\n')
    file.write(f'BTC Price = ${coin_list[0]}\n\n ETH Price = ${coin_list[3]}\n\n\n')
    file.write(f'BTC Holdings = {coin_list[2]}BTC\n\n ETH holdings = {coin_list[5]}ETH \n\n')

    df = pd.DataFrame({'Date':[str(today)],'Value':[str(vals)]})
    
    wb = load_workbook(filename = 'value.xlsx')
    ws = wb['Sheet']

    newRowLoc = ws.max_row + 1
    ws.cell(column=1, row = newRowLoc, value =str(today))
    ws.cell(column=2, row = newRowLoc, value =str(vals))
    wb.save(filename='value.xlsx')
    wb.close()

    t.sleep(1)

main()






