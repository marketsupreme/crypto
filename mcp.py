#!/usr/bin/env python
# coding: utf-8

from requests import get, patch
import json
import time as t
from datetime import date, datetime
import calendar
import pandas as pd
from openpyxl import load_workbook

def getCoinValue(coinList) -> dict():

    #nested dictionary will store each coin's information
    portfolio = {k:{} for k in coinList}

    #getting all crypto prices from Nomics and storing them in a JSON
    prices = get(f'https://api.nomics.com/v1/currencies/ticker?key=ea386addbac03f4bb67ceb1f333a8d0a&ids={",".join(coinList)}&interval=1d&convert=USD&per-page=100&page=1')
    priceData = prices.json()

    #adding the prices of each coin to portfolio dictionary
    for i in range(len(coinList)):
        portfolio[coinList[i]]['price'] = round(float(priceData[i]['price']),2)

    #getting ethereum holdings and storing in a JSON
    ethWallet = get('https://api.ethplorer.io/getAddressInfo/0xed8b4b3ba4fd5a175613859cab6ab8f010276a3a?apiKey=freekey')
    ethData = ethWallet.json()

    #adding the holdings to portfolio dictionary
    portfolio['ETH']['holdings']  = ethData['ETH']['balance']
    portfolio['BTC']['holdings'] = 1.06
    portfolio['DOGE']['holdings'] = 1809.826

    #adding the value to portfolio dictionary
    for i in range(len(coinList)):
        portfolio[coinList[i]]['value'] = portfolio[coinList[i]]['holdings']*portfolio[coinList[i]]['price']

    return portfolio

def getStockValue(stockDict) -> dict():

    stockKey = '10SVU9Y1PENCIBZN'
    portfolio = {k:{} for k in stockDict.keys()}

    for ticker in stockDict.keys():
        prices = get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={stockKey}')
        priceData = prices.json()
        portfolio[ticker]['price'] = round(float(priceData['Global Quote']["05. price"]),2)
        portfolio[ticker]['holdings'] = stockDict[ticker]
        portfolio[ticker]['value'] = portfolio[ticker]['holdings']*portfolio[ticker]['price']
    
    return portfolio

def main():

    #stocks and crypto variables, available to be updated at anytime
    Coins = ['BTC', 'ETH', 'DOGE']
    Stocks = {'TSLA': 1, 'SMG': 10}

    #opening the readme to be displayed on Github pages
    file = open('README.md', 'w')

    #grabbing date information
    today = date.today().strftime("%m/%d/%y")
    time = datetime.now().strftime("%H:%M:%S")
    day = calendar.day_name[date.today().weekday()]

    #calling getValue function to find portfolio value
    coinDict = getCoinValue(Coins)
    stockDict = getStockValue(Stocks)

    #formating and rounding the total portfolio values
    coinValue = "{:,}".format(round(sum(coin['value'] for coin in coinDict.values() if coin),2))
    stockValue = "{:,}".format(round(sum(stock['value'] for stock in stockDict.values() if stock),2))
    totalValue = coinValue+stockValue

    #writing to the readme with value and timestamp
    file.write(f'# Value: ${totalValue}\n\n')
    file.write(f'## Crypto Value: ${coinValue}\n\n')
    file.write(f'## Stock Value: ${stockValue}\n\n')
    file.write(f'#### {day}, {today} @ {time} \n\n')

    #Coin prices
    for coin in Coins:
        file.write(f"{coin} Price = ${'{:,}'.format(coinDict[coin]['price'])}\n")
    file.write('\n\n')
    
    #Coin holdings
    for coin in Coins:
        file.write(f"{coin} Holdings = {coinDict['BTC']['holdings']}{coin}\n")
    file.write('\n\n')

    #Stock prices
    for stock in Stocks:
        file.write(f"{stock} Price = ${'{:,}'.format(stockDict[stock]['price'])}\n")
    file.write('\n\n')
    
    #Stock holdings
    for coin in Coins:
        file.write(f"{coin} Holdings = {coinDict['BTC']['holdings']}{coin}\n")
    file.write('\n\n')

    df = pd.DataFrame({'Date':[str(today)],'Value':[totalValue]})
    
    #writing the portfolio value to an excel file for data compilation
    wb = load_workbook(filename = 'value.xlsx')
    ws = wb['Sheet']
    newRowLoc = ws.max_row + 1
    ws.cell(column=1, row = newRowLoc, value =str(today))
    ws.cell(column=2, row = newRowLoc, value =str(totalValue))
    wb.save(filename='value.xlsx')
    wb.close()

    t.sleep(1)

main()
