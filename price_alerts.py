import time
import os
from datetime import datetime
import requests
from portfolio import API_KEY, convert


already_hit_targets = []  # add coins to a list that will be checked to make sure alerts are not repeated


def alerts_on():
    while True:
        with open('alerts.txt') as alerts:
            for line in alerts:
                coin, amount = line.split(",")
                coin = coin.upper()

                ticker_url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?CMC_PRO_API_KEY={API_KEY}&symbol={coin}&convert={convert}"

                request = requests.get(ticker_url)
                results = request.json()

                currency = results['data'][coin]
                name = currency['name']
                price = currency['quote'][convert]['price']
                last_updated = currency["quote"][convert]['last_updated']
                date_string = datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%fZ")

                if float(price) > float(amount) and coin not in already_hit_targets:
                    os.system('say ' + name + 'has hit' + f"{price:.0f}")
                    print(name + ' has reached ' + f"${price:.0f}" + ' at ' + f"{date_string}")
                    already_hit_targets.append(coin)

            print('Prices checked at ' + f"{date_string}")
            print('----')
        time.sleep(60)  # checks prices once per minute
