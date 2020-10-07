# crypto_portfolio
 
This app uses TKinter's GUI to show a range of assets in ones cryptocurrency portfolio, connecting to live data from CoinMarketCap's API.

<img width="1000" alt="crypto_portfolio_v2" src="https://user-images.githubusercontent.com/68865367/95259026-76cb2d00-081e-11eb-96fe-0241215c987f.png">

The GUI has built in buttons to refresh prices, create a pie graph of the worth of assets in a portfolio, export todays data to Excel. 
<img width="400" alt="crypto_portfolio_v5" src="https://user-images.githubusercontent.com/68865367/95259634-623b6480-081f-11eb-8183-a5bbe8026c67.png">


Another button can turn price alerts on, where the app will monitor prices every minute and the OS will sound when a coin has hit a certain price.


The portfolio assets/amounts and price alerts are configureable by the user.

You can set coin symbol and USD$ price you wish the computer to alert you at, in the alerts.txt file

```
btc,10500
eth,350
link,12.50
xrp,1.24
trx,0.065
```

If the target price has not already been hit, the OS will voice the alert, and then add the coin to a list of hit targets. 

```python
if float(price) > float(amount) and coin not in already_hit_targets:
    os.system('say ' + name + 'has hit' + f"{price:.0f}")
```


User can input what crpytocurrency coins they have, how many units, and what price they originally paid per coin in the portfolio.py file.
```python
my_portfolio = [
        {
        "symbol": "BTC",
        "amount_owned": 0.75,
        "price_paid_per_unit": 5000
        },
        {
        "symbol": "ETH",
        "amount_owned": 3,
        "price_paid_per_unit": 200
        },
        {
        "symbol": "LTC",
        "amount_owned": 5,
        "price_paid_per_unit": 75
        },
        {
        "symbol": "XRP",
        "amount_owned": 0,
        "price_paid_per_unit": 0
        },
        {
        "symbol": "LINK",
        "amount_owned": 500,
        "price_paid_per_unit": 3
        },
]
```

Lastly the user can save export the values to an excel spreadsheet saved under todays date to keep a track of the changes to their portfolio over days/weeks/months.

<img width="750" alt="crypto_portfolio_v6 copy" src="https://user-images.githubusercontent.com/68865367/95303808-96447300-087b-11eb-9886-ad85f26a7ead.png">

