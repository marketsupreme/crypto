#!/usr/bin/env python
# coding: utf-8

from requests import get
import json
import time as t
from datetime import date, datetime
import calendar
import pandas as pd
from openpyxl import load_workbook


#global coins variable, available to be updated at anytime
coins = ['BTC', 'ETH', 'DOGE']


def getValue(coinList):

    #nested dictionary will store each coin's information
    portfolio = {k: {} for k in coinList}

    #getting all crypto prices from Nomics and storing them in a JSON
    prices = get('https://api.nomics.com/v1/currencies/ticker?key=ea386addbac03f4bb67ceb1f333a8d0a&ids=BTC,ETH,DOGE&interval=1d&convert=USD&per-page=100&page=1')
    data = prices.json()

    print(portfolio)

    #adding the prices of each coin to portfolio dictionary
    for i in range(len(coinList)):
        portfolio[coinList[i]]['price'] = round(float(data[i]['price']),2)

    #getting ethereum holdings and storing in a JSON
    ethWallet = get('https://api.ethplorer.io/getAddressInfo/0xed8b4b3ba4fd5a175613859cab6ab8f010276a3a?apiKey=freekey')
    data = ethWallet.json()

    #adding the holdings to portfolio dictionary
    portfolio['ETH']['holdings']  = data['ETH']['balance']
    portfolio['BTC']['holdings'] = 1.06
    portfolio['DOGE']['holdings'] = 1809.826

    #adding the value to portfolio dictionary
    for i in range(len(coinList)):
        portfolio[coinList[i]]['value'] = portfolio[coinList[i]]['holdings']*portfolio[coinList[i]]['price']

    return portfolio


def main():

    file = open('README.md', 'w')
    today = date.today().strftime("%m/%d/%y")
    time = datetime.now().strftime("%H:%M:%S")
    day = calendar.day_name[date.today().weekday()]

    coinDict = getValue(coins)

    vals = "{:,}".format(round(coinDict['ETH']['value']+coinDict['BTC']['value']+coinDict['DOGE']['value'],2))
    
    file.write(f'# Value: ${vals}\n\n')
    file.write(f'#### {day}, {today} @ {time} \n\n')
    file.write(f"BTC Price = ${coinDict['BTC']['price']}\n\ ETH Price = ${coinDict['ETH']['price']}\n\ DOGE Price = ${coinDict['DOGE']['price']}\n\n\n")
    file.write(f"BTC Holdings = {coinDict['BTC']['holdings']}BTC\n\n ETH holdings = {coinDict['ETH']['holdings']}ETH\n\n DOGE Holdings = {coinDict['DOGE']['holdings']}DOGE\n\n")

    df = pd.DataFrame({'Date':[str(today)],'Value':[vals]})
    
    wb = load_workbook(filename = 'value.xlsx')
    ws = wb['Sheet']

    newRowLoc = ws.max_row + 1
    ws.cell(column=1, row = newRowLoc, value =str(today))
    ws.cell(column=2, row = newRowLoc, value =str(vals))
    wb.save(filename='value.xlsx')
    wb.close()

    t.sleep(1)

main()






