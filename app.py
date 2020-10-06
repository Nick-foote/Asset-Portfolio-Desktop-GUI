import tkinter as tk
import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime
import xlsxwriter
from portfolio import my_portfolio
from price_alerts import alerts_on
from portfolio import API_KEY, convert

date = datetime.today().strftime('%Y_%m_%d')  # adding today's' date to filename
file_name = f'prices_{date}.xlsx'

### Excel setup ##
price_workbook = xlsxwriter.Workbook(file_name)
price_sheet = price_workbook.add_worksheet()
price_sheet.write('A1', 'Name')
price_sheet.write('B1', 'Current Price')
price_sheet.write('C1', 'Amount Paid Per Unit')
price_sheet.write('D1', 'Amount Invested')
price_sheet.write('E1', 'Current Worth')
price_sheet.write('F1', 'Profit/Loss')
price_sheet.write('G1', 'P/L %')

written = False  # to be changed at the end in order to close and write to the excel file



def red_green(amount):
    """used for text colour to indicate negative or positive change"""
    if amount > 0:
        return "green"
    elif amount == 0:
        return "black"
    else:
        return "red"


def graph(pie_labels, pie_sizes):
    """will plot a pie graph representing each coins value"""
    labels = pie_labels
    sizes = pie_sizes
    patches, texts = plt.pie(sizes, shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


class Portfolio(tk.Tk):
    def __init__(self):
        super().__init__()

        container = tk.Frame(self)
        container.grid()

        ## Header Section ##
        header_name = tk.Label(container, text="Name", bg="azure2", font="Verdana 12 bold")
        header_name.grid(row=0, column=0, sticky="NSEW")

        header_current_price = tk.Label(container, text="Current_Price", bg="azure2", font="Verdana 12 bold")
        header_current_price.grid(row=0, column=1, sticky="NSEW")

        header_1hr_change = tk.Label(container, text="1hr Change", bg="azure2", font="Verdana 12 bold")
        header_1hr_change.grid(row=0, column=2, sticky="NSEW")

        header_24hr_change = tk.Label(container, text="24hr Change", bg="azure2", font="Verdana 12 bold")
        header_24hr_change.grid(row=0, column=3, sticky="NSEW")

        header_7day_change = tk.Label(container, text="7day Change", bg="azure2", font="Verdana 12 bold")
        header_7day_change.grid(row=0, column=4, sticky="NSEW")

        header_amount_paid = tk.Label(container, text="Amount Paid Per Coin", bg="azure2", font="Verdana 12 bold")
        header_amount_paid.grid(row=0, column=5, sticky="NSEW")

        header_amount_invested = tk.Label(container, text="Amount Invested", bg="azure2", font="Verdana 12 bold")
        header_amount_invested.grid(row=0, column=6, sticky="NSEW")

        header_current_worth = tk.Label(container, text="Current Worth", bg="azure2", font="Verdana 12 bold")
        header_current_worth.grid(row=0, column=7, sticky="NSEW")

        header_coin_balance = tk.Label(container, text="Profit/Loss", bg="azure2", font="Verdana 12 bold")
        header_coin_balance.grid(row=0, column=8, sticky="NSEW")

        header_coin_balance_percent = tk.Label(container, text="P/L %", bg="azure2", font="Verdana 12 bold")
        header_coin_balance_percent.grid(row=0, column=9, ipadx=10, sticky="NSEW")

        self.lookup(container)

        ## Buttons ##
        alerts_button = tk.Button(
            container,
            text="Turn Alerts On",
            command=alerts_on
        )
        alerts_button.grid(row=self.row_count + 1, column=6, padx=5, pady=10, sticky="WE")

        graph_button = tk.Button(
            container,
            text="Portfolio Pie Graph",
            command=lambda: graph(self.pie_labels, self.pie_sizes)
        )
        graph_button.grid(row=self.row_count + 1, column=7, padx=5, pady=10, sticky="WE")

        refresh_button = tk.Button(
            container,
            text="Refresh Prices",
            command=lambda: self.lookup(container)
        )
        refresh_button.grid(row=self.row_count + 1, column=8, padx=10, pady=10, sticky="WE")

        write_excel_button = tk.Button(
            container, text="Write to Excel",
            command=lambda: self.lookup(container, write_to_excel=True)
        )
        write_excel_button.grid(row=self.row_count + 1, column=9, padx=10, pady=10, sticky="WE")

        self.title(f"Crypto Currency Portfolio -  P/L: {float(self.portfolio_change_percent):.2f}%")

    def lookup(self, container, write_to_excel=False):
        """This API request will happen every time the user clicks the refresh button.
        API Account request limit is 10 per minute"""
        api_request = requests.get(
            f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY={API_KEY}&start=1&limit=100&convert={convert}"
        )
        api = json.loads(api_request.content)

        portfolio_profit_loss = 0
        starting_amount = 0
        portfolio_value = 0

        self.row_count = 1
        excel_counter = 1

        ## labels and quantities used for pie graph
        self.pie_labels = []
        self.pie_sizes = []

        for x in api["data"]:
            for coin in my_portfolio:
                if coin["symbol"] == x["symbol"]:
                    total_paid = float(coin["amount_owned"] * float(coin["price_paid_per_unit"]))
                    current_value = float(coin["amount_owned"] * float(x["quote"][convert]["price"]))

                    name = x["name"]
                    price = f"{float(x['quote'][convert]['price']):,.2f}"
                    amount_paid_per = f"{float(coin['price_paid_per_unit']):,.0f}"

                    coin_balance = current_value - total_paid
                    try:
                        coin_balance_percent = (current_value - total_paid) / total_paid * 100
                    except ZeroDivisionError:
                        coin_balance_percent = 0

                    portfolio_profit_loss += coin_balance
                    starting_amount += total_paid
                    portfolio_value += current_value

                    name_label = tk.Label(container, text=name, bg="white")
                    name_label.grid(row=self.row_count, column=0, sticky="NSEW")

                    current_price = tk.Label(container, text=price, bg="silver")
                    current_price.grid(row=self.row_count, column=1, sticky="NSEW")

                    change_1hr = tk.Label(
                        container,
                        text=f'{float(x["quote"][convert]["percent_change_1h"]):.2f}%',
                        bg="white", fg=red_green(float(x["quote"][convert]["percent_change_1h"]))
                    )
                    change_1hr.grid(row=self.row_count, column=2, sticky="NSEW")

                    change_24hr = tk.Label(
                        container,
                        text=f'{float(x["quote"][convert]["percent_change_24h"]):.2f}%',
                        bg="silver",
                        fg=red_green(float(x["quote"][convert]["percent_change_24h"]))
                    )
                    change_24hr.grid(row=self.row_count, column=3, sticky="NSEW")

                    change_7day = tk.Label(
                        container,
                        text=f'{float(x["quote"][convert]["percent_change_7d"]):.2f}%',
                        bg="white", fg=red_green(float(x["quote"][convert]["percent_change_7d"]))
                    )
                    change_7day.grid(row=self.row_count, column=4, sticky="NSEW")

                    amount_paid_per_label = tk.Label(container, text=f"${amount_paid_per}", bg="silver")
                    amount_paid_per_label.grid(row=self.row_count, column=5, sticky="NSEW")

                    amount_invested_label = tk.Label(container, text=f"${total_paid:,}", bg="white")
                    amount_invested_label.grid(row=self.row_count, column=6, sticky="NSEW")

                    current_worth = tk.Label(container, text=f"${current_value:,.2f}", bg="silver")
                    current_worth.grid(row=self.row_count, column=7, sticky="NSEW")

                    coin_balance_label = tk.Label(
                        container,
                        text=f"${coin_balance:,.2f}",
                        bg="white",
                        fg=red_green(coin_balance)
                    )
                    coin_balance_label.grid(row=self.row_count, column=8, sticky="NSEW")

                    coin_balance_percent_label = tk.Label(
                        container,
                        text=f"{coin_balance_percent:.2f}%",
                        bg="silver",
                        fg=red_green(coin_balance_percent)
                    )
                    coin_balance_percent_label.grid(row=self.row_count, column=9, sticky="NSEW")

                    self.row_count += 1

                    # Ignores coins in portfolio where no amount is owned.
                    if coin["amount_owned"] > 0:
                        self.pie_labels.append(x["name"])
                        self.pie_sizes.append(current_value)

                    if write_to_excel is True:
                        global written
                        written = True
                        price_sheet.write(excel_counter, 0, name)
                        price_sheet.write(excel_counter, 1, price)
                        price_sheet.write(excel_counter, 2, amount_paid_per)
                        price_sheet.write(excel_counter, 3, total_paid)
                        price_sheet.write(excel_counter, 4, f"{current_value:,.2f}")
                        price_sheet.write(excel_counter, 5, f"{coin_balance:,.2f}")
                        price_sheet.write(excel_counter, 6, f"{coin_balance_percent:,.2f}")
                        price_sheet.write(excel_counter + 1, 0, f"Portfolio value: ${portfolio_value:,.2f}")
                        price_sheet.write(excel_counter + 2, 0, f"Profit/Loss: ${portfolio_profit_loss:,.2f} ({self.portfolio_change_percent:,.2f}%)")

                        excel_counter += 1

        self.portfolio_change_percent = (portfolio_value - starting_amount) / starting_amount * 100

        portfolio_current_value = tk.Label(container, text=f"Portfolio Value: ${float(portfolio_value):,.2f}")
        portfolio_current_value.grid(row=self.row_count, pady=(10, 0), column=0, sticky="W", padx=10)

        portfolio_p_and_l = tk.Label(
            container,
            text=f"P/N: ${float(portfolio_profit_loss):,.2f}  ({float(self.portfolio_change_percent):,.2f}%)",
            fg=red_green(self.portfolio_change_percent)
        )
        portfolio_p_and_l.grid(row=self.row_count + 1, column=0, sticky="W", padx=10)

        api = ""  # reset api data to nothing


app = Portfolio()

app.mainloop()

if written is True:     # will only close the workbook if the write to excel button has been pressed
    price_workbook.close()
