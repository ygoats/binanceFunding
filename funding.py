#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 05:17:10 2020

@ygoats
"""

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceRequestException

import apiHighs

import telegram_send

from time import sleep

from datetime import datetime, timedelta

from requests import exceptions

symbolA = []
symbolB = []

def Main():  
    now = datetime.now()
    t = now.strftime("%m/%d/%Y, %H:%M:%S")
    
    print("Connection Established")
    print(str(t))
    
    client = Client(apiHighs.APIKey, apiHighs.SecretKey)
    
    funding = client.futures_mark_price()
    lenFunding = len(funding)
    
    #print(funding)
    progStart = True
    
    while progStart == True:
        progress = False
        try:
            sleep(10)
            now = datetime.now()
            t = now.strftime("%H:%M:%S")
            
            symbolA = []
            symbolB = []
            
            client = Client(apiHighs.APIKey, apiHighs.SecretKey)
        
            funding = client.futures_mark_price()
            lenFunding = len(funding)
        except Exception as e:
            print(e)
        
        if t >= "00:00:00" and t <= "00:00:30":
            progress = True
        if t >= "06:00:00" and t <= "06:00:30":
            progress = True
        if t >= "12:00:00" and t <= "12:00:30":
            progress = True
        if t >= "18:00:00" and t <= "18:00:30":
            progress = True
            
        if progress == True:
            for a in range(lenFunding):

                fundA = float(funding[a]['lastFundingRate'])
                fundB = float(fundA) * 100
                if fundB > 0.01:
                    symbolA.append(str("{:.4f}".format(float(fundB))) + " " + str(funding[a]['symbol']))
                if fundB < -0.01:
                    symbolB.append(str("{:.4f}".format(float(fundB))) + " " + str(funding[a]['symbol']))
                            
            symbolA.sort()
            symbolB.sort()
                
            #print(symbolA)
            print(symbolB)
            
            lenSymbolA = len(symbolA)
            print(lenSymbolA)
            topPositiveFund = []
            
            if lenSymbolA > 7:
                
                for ab in range(7):
                    topPositiveFund.append(symbolA[(lenSymbolA-1)-ab])
                    
            lenSymbolB = len(symbolB)
            print(lenSymbolB)
            topNegativeFund = []
                
            if lenSymbolB > 7:
            
                for ac in range(7):
                    topNegativeFund.append(symbolB[(lenSymbolB-1)-ac])
                    
                #print(topPositiveFund)
                print(topNegativeFund)
                
            if lenSymbolA > 7:
                
                telegram_send.send(disable_web_page_preview=True, conf='user1.conf',messages=[ \
                                                "Top 7 Positive Funding on Binance" + "\n" + \
                                                topPositiveFund[0] + "\n" + \
                                                topPositiveFund[1] + "\n" + \
                                                topPositiveFund[2] + "\n" + \
                                                topPositiveFund[3] + "\n" + \
                                                topPositiveFund[4] + "\n" + \
                                                topPositiveFund[5] + "\n" + \
                                                topPositiveFund[6] + "\n"  \
                                                ])
                progress = False
                sleep(100)
            if lenSymbolB > 7:

                telegram_send.send(disable_web_page_preview=True, conf='user1.conf',messages=[ \
                                                "Top 7 Negative Funding on Binance" + "\n" + \
                                                topNegativeFund[0] + "\n" + \
                                                topNegativeFund[1] + "\n" + \
                                                topNegativeFund[2] + "\n" + \
                                                topNegativeFund[3] + "\n" + \
                                                topNegativeFund[4] + "\n" + \
                                                topNegativeFund[5] + "\n" + \
                                                topNegativeFund[6] + "\n"  \
                                                ])
                progress = False
                sleep(100)
                    
if __name__ == '__main__':
    Main()
