#!/usr/bin/env python
# coding: utf-8

import requests
import time


def telegram_sendText(bot_credentials, bot_message):
    bot_token = bot_credentials[0]
    bot_chatID = bot_credentials[1]
    send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+bot_chatID+'&text='+bot_message
    response = requests.get(send_text)
    return response.json()


def token_data(token):
    liquidity_address = input('Enter '+token+' Uniswap liquidity pool address\n>')
    token_address = input('Enter '+token+' contract address\n>')
    
    return liquidity_address,token_address


def price_pull(api, liquidity_address, token_address):
    weth_address = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    while True:
        try:
            eth_balance = int(requests.get('https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress='+weth_address+'&address='+liquidity_address+'&tag=latest&apikey='+api).json()['result'])/1000000000000000000
            token_balance = int(requests.get('https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress='+token_address+'&address='+liquidity_address+'&tag=latest&apikey='+api).json()['result'])/1000000000000000000
            eth_usd = float(requests.get('https://api.etherscan.io/api?module=stats&action=ethprice&apikey='+api).json()['result']['ethusd'])
        except json.decoder.JSONDecodeError:
            continue
        else:
            break
    token_usd = round(eth_balance/token_balance*eth_usd, 2)
    
    return token_usd


def price_targets(token):
    while True:
        try:
            buy_price = float(input('Enter '+token+' Buy Target\n>'))
        except ValueError:
            print('Must be float\n')
            continue
        else:
            print('Buy Target Set\n')
            break
    
    while True:
        try:
            sell_price = float(input('Enter '+token+' Sell Target\n>'))
        except ValueError:
            print('Must be float\n')
            continue
        else:
            print('Sell Target Set\n')
            break
    
    return buy_price,sell_price


def set_alert(token, buy_price, sell_price, liquidity_pool, contract):
    token_usd = price_pull(etherscan_api, liquidity_pool, contract)
    if token_usd <= buy_price:
        msg = f'''
{token} is at/below Buy Target of ${buy_price}
Current {token} Price: ${token_usd}'''
    elif token_usd >= sell_price:
        msg = f'''
{token} is at/above Sell Target of ${sell_price}
Current {token} Price: ${token_usd}'''
    else:
        msg = None
    
    return msg


etherscan_api = input('Enter etherscan API Key\n>')
token_name = input('Enter token name\n>')
addresses = token_data(token_name)
bot_credentials = (input('Enter Telegram Bot Access Token\n>'), input('Telegram User ID\n>'))
targets = price_targets(token_name)


while True:
    msg = set_alert(token_name, targets[0], targets[1], addresses[0], addresses[1])
    if msg:
        telegram_sendText(bot_credentials, msg)
        time.sleep(60*60*24)
    time.sleep(5)

