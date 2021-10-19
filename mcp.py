#!/usr/bin/env python
# coding: utf-8

from requests import get,request
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


    url = "https://yh-finance.p.rapidapi.com/stock/v2/get-summary"

    querystring = {"symbol":','.join(stockDict)}

    headers = {
        'x-rapidapi-host': "yh-finance.p.rapidapi.com",
        'x-rapidapi-key': "982db98a4bmsh94fff9031be156dp198c9fjsn49f0b840ebbc"
        }

    prices = request("GET", url, headers=headers, params=querystring)

    priceData = prices.json()
    file = open('prices.json', 'w')
    file.write(priceData)






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
    #coinDict = getCoinValue(Coins)
    stockDict = getStockValue(Stocks)

    #formating and rounding the total portfolio value
    vals = "{:,}".format(round(coinDict['ETH']['value']+coinDict['BTC']['value']+coinDict['DOGE']['value'],2))
    
    #writing to the readme with value, timestamp, current price info and holdings
    file.write(f'# Value: ${vals}\n\n')
    file.write(f'#### {day}, {today} @ {time} \n\n')
    file.write(f"BTC Price = ${'{:,}'.format(coinDict['BTC']['price'])}\n\ ETH Price = ${'{:,}'.format(coinDict['ETH']['price'])}\n\ DOGE Price = ${'{:,}'.format(coinDict['DOGE']['price'])}\n\n\n")
    file.write(f"BTC Holdings = {coinDict['BTC']['holdings']}BTC\n\n ETH holdings = {coinDict['ETH']['holdings']}ETH\n\n DOGE Holdings = {coinDict['DOGE']['holdings']}DOGE\n\n")

    df = pd.DataFrame({'Date':[str(today)],'Value':[vals]})
    
    #writing the portfolio value to an excel file for data compilation
    wb = load_workbook(filename = 'value.xlsx')
    ws = wb['Sheet']
    newRowLoc = ws.max_row + 1
    ws.cell(column=1, row = newRowLoc, value =str(today))
    ws.cell(column=2, row = newRowLoc, value =str(vals))
    wb.save(filename='value.xlsx')
    wb.close()

    t.sleep(1)

main()
