"""
File: extension.py
Author: Yinan Gordon Liu
------------------
This program integrates stock data scraping using 'yfinance' and creates a
simple text-based stock trading simulator game.

Players can input an initial cash amount and practice buying, selling, or
holding positions using real historical data from Apple Inc. (AAPL).

"""

import yfinance as yf
import csv
from world_model_test import Portfolio


def main():
    apple_data_list = []

    apple_data = yf.Ticker("AAPL")
    apple_stock_data_1_y = apple_data.history(period = "1y")
    apple_stock_data_1_y.to_csv("AppleStock_1_year.csv")
    with open("AppleStock_1_year.csv", "r") as f:
        content = csv.DictReader(f)

        for row in content:
            if row["Close"] != "":
                apple_data_list.append(row)

    print("-----------Print the Stock Information------------")
    for row in apple_data_list:
        print(row)
    print(f"The close price in {apple_data_list[0]['Date']} is {apple_data_list[0]['Close']}")



    print("Welcome to the 1 year Apple Stock Trading Simulator!")
    print("------------------------------------------------------------------")

    initial_cash = float(input("Please enter your initial cash: "))
    cash = initial_cash
    shares_hold = 0
    total_days = len(apple_data_list)

    apple_portfolio = Portfolio(initial_cash)


    for day in range(1, total_days + 1):
        stock_price = round(float(apple_data_list[day - 1]["Close"]), 2)
        print()
        print(f"=============== DAY {day} of {total_days} ==================")
        print(f"Current Apple Stock Price: ${stock_price} per share")
        print(f"Your Wallet: ${cash} | Shares Owned: {shares_hold} shares")
        print("---------------------------------------------")

        print("What would you like to do?")
        print("1: Buy Apple Stock")
        print("2: Sell Apple Stock")
        print("3: Hold (Do nothing for today)")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            shares_to_buy = int(input("How many shares of Apple Stock do you want to buy? "))
            apple_portfolio.buy(shares_to_buy, stock_price)
            
        elif choice == "2":
            shares_to_sell = int(input("How many shares of Apple Stock do you want to sell? "))
            apple_portfolio.sell(shares_to_sell, stock_price)

        elif choice == "3":
            apple_portfolio.hold()

        else:
            print("Invalid choice! You cannot operate today because you're hesitating too much!")

        cash = apple_portfolio.cash
        shares_hold = apple_portfolio.shares

        

    final_stock_price = round(float(apple_data_list[total_days - 1]["Close"]), 2)
    final_payout = apple_portfolio.shares * final_stock_price
    cash += final_payout

    print()
    print("================== MARKET CLOSED ==================")
    print("The 1 year market is up! Your remaining shares were calculated as cash at today's final price.")
    print(f"Your final net worth is: ${cash}")

    profit = cash - initial_cash
    if profit > 0:
        print(f"Great job! You made a total profit of ${profit}!")
    elif profit < 0:
        print(f"Sorry! You lost ${-1 * profit}. The market was tough!")
    else:
        print("You did not win or loose!")

# This provided line is required at the end of a Python file
# to call the main() function.
if __name__ == "__main__":
    main()
