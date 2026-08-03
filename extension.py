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
import json
from world_model_test import Portfolio
from notopenai import NotOpenAI

CLIENT = NotOpenAI(api_key="e0e0c8e6-de84-4f8e-b407-9d408e470f0d") # Use my NotOpenAI client



def get_stock_information():
    """
    Downloads 2 years of Apple (AAPL) historical stock data using yfinance,
    saves it to a CSV file, and reads it back into a list of dictionaries.
    Rows with an empty "Close" value are skipped.

    Returns:
        A list of dictionaries, where each dictionary is one trading day
        with keys such as "Date", "Open", "High", "Low", "Close", "Volume".
    """
    apple_data_list = []

    apple_data = yf.Ticker("AAPL")
    apple_stock_data_2_y = apple_data.history(period = "2y")
    apple_stock_data_2_y.to_csv("AppleStock_2_year.csv")
    with open("AppleStock_2_year.csv", "r") as f:
        content = csv.DictReader(f)

        for row in content:
            if row["Close"] != "":
                apple_data_list.append(row)
                
    print("-----------Print the Stock Information------------")
    for row in apple_data_list:
        print(row)
    print(f"The close price in {apple_data_list[0]['Date']} is {apple_data_list[0]['Close']}")
    return apple_data_list

def print_relavant_information(day, total_days, cash, shares_hold, average_cost, recent_stock_prices, five_days_average_price, twenty_days_average_price, apple_data_list):
    """
    Prints the daily dashboard for the player: the current date, portfolio
    status (cash, shares held, average cost), today's closing price, the
    previous four days' closing prices, and the 5-day and 20-day averages.

    Parameters:
        day: the index of the current trading day in apple_data_list
        total_days: the total number of trading days available
        cash: the player's current cash balance
        shares_hold: the number of shares the player currently owns
        average_cost: the player's average cost per share
        recent_stock_prices: closing prices from newest to oldest (20 days)
        five_days_average_price: the average of the last 5 closing prices
        twenty_days_average_price: the average of the last 20 closing prices
        apple_data_list: the full stock data, used here to look up the date
    """
    print()
    print(f"=============== DAY {day} of {total_days} ==================")
    print(f"Today is {apple_data_list[day - 1]['Date'][:10]}")
    print(f"Your Wallet: ${round(cash, 2)} | Shares Owned: {shares_hold} shares")
    print(f"Your Average Cost: ${average_cost}")

    print("---------------------------------------------")
    print(f"Today's Closing Price: ${recent_stock_prices[0]} per share")
    for i in range(1, 5):
        print(f"Day {day - i}: ${recent_stock_prices[i]} per share")
    print(f"5-Day Average: ${five_days_average_price} | 20-Day Average: ${twenty_days_average_price}")
    print("---------------------------------------------")

def get_gpt_decision(portfolio, current_price, recent_prices, twenty_days_avg, days_left):
    """
    Asks ChatGPT for a trading suggestion based on the current market data
    and the player's portfolio. The prompt constrains the model so that the
    suggested number of shares never exceeds what the player can afford
    (for buying) or currently owns (for selling).

    Parameters:
        portfolio: the Portfolio object holding cash, shares, and cost basis
        current_price: today's closing price
        recent_prices: the last 5 closing prices, newest to oldest
        twenty_days_avg: the 20-day average closing price
        days_left: how many trading days remain in the simulation

    Returns:
        A dictionary with three keys:
            "action" - one of "buy", "sell", or "hold"
            "shares" - the suggested number of shares (0 when holding)
            "reason" - a short explanation from the model
    """

    max_buy = int(portfolio.cash / current_price)
    chat_completion = CLIENT.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"You are a stock trading advisor for Apple (AAPL). "
                           f"Today's price is ${current_price}. "
                           f"The last 5 closing prices (newest to oldest) are: {recent_prices}. "
                           f"The 20-day average price is ${twenty_days_avg}. "
                           f"There are {days_left} trading days left in the simulation. "
                           f"I currently have ${round(portfolio.cash, 2)} in cash and hold "
                           f"{portfolio.shares} shares at an average cost of "
                           f"${round(portfolio.average_cost(), 2)} per share. "
                           f"Reply ONLY in json with keys: action, shares, reason. "
                           f"action must be exactly one of: buy, sell, hold. "
                           f"If action is buy, shares must be an integer no greater than {max_buy}. "
                           f"If action is sell, shares must be an integer no greater than {portfolio.shares}. "
                           f"If action is hold, shares must be 0. "
                           f"Keep reason under 20 words.",
            }
        ],
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"}
    )
    response_str = chat_completion.choices[0].message.content
    return json.loads(response_str)


def main():

    apple_data_list = get_stock_information()

    #initialize every things
    print("Welcome to the 1 year Apple Stock Trading Simulator!")
    print("------------------------------------------------------------------")
    initial_cash = float(input("Please enter your initial cash: "))
    cash = initial_cash
    shares_hold = 0
    total_days = len(apple_data_list) # I just wanna start from the trading day 1 year ago.
    start_day = total_days - 250 # This is a approximate number, I can make it more accurate if I have time.
    
    apple_portfolio = Portfolio(initial_cash)

    for day in range(start_day, total_days):
        #Calculate recent stock prices and process the data
        recent_stock_prices = []
        
        for i in range(1, 21):
            price = round(float(apple_data_list[day - i]["Close"]), 2)
            recent_stock_prices.append(price)

        five_days_average_price = round(sum(recent_stock_prices[:5]) / 5, 2)
        twenty_days_average_price = round(sum(recent_stock_prices[:20]) / 20, 2)
        average_cost = apple_portfolio.average_cost()

        print_relavant_information(day, total_days, cash, shares_hold, average_cost, recent_stock_prices, five_days_average_price, twenty_days_average_price, apple_data_list)

        print("...Waiting for AI suggestion...")
        gpt_decision = get_gpt_decision(apple_portfolio, recent_stock_prices[0], recent_stock_prices[:5], twenty_days_average_price, total_days - day)
        action_to_choice = {"buy": "1", "sell": "2", "hold": "3"}
        suggested_action = action_to_choice[gpt_decision["action"]]
        suggested_amount = gpt_decision["shares"]
        suggested_reason = gpt_decision["reason"]

        print(f"[AI Suggests] {gpt_decision['action']} {suggested_amount} shares — {suggested_reason}")
        print()

        print("What would you like to do? Press 'Enter' to accept the AI suggestion.")
        print("1: Buy Apple Stock")
        print("2: Sell Apple Stock")
        print("3: Hold (Do nothing for today)")

        choice = input("Enter your choice (Enter/1/2/3): ")

        # If the user presses Enter, accept the AI suggestion
        if choice == "":
            if suggested_action == "1":
                apple_portfolio.buy(suggested_amount, recent_stock_prices[0])
            if suggested_action == "2":
                apple_portfolio.sell(suggested_amount, recent_stock_prices[0])
            if suggested_action == "3":
                apple_portfolio.hold()

        elif choice == "1":
            shares_to_buy = int(input("How many shares of Apple Stock do you want to buy? "))
            apple_portfolio.buy(shares_to_buy, recent_stock_prices[0])

        elif choice == "2":
            shares_to_sell = int(input("How many shares of Apple Stock do you want to sell? "))
            apple_portfolio.sell(shares_to_sell, recent_stock_prices[0])

        elif choice == "3":
            apple_portfolio.hold()

        else:
            print("Invalid choice! You cannot operate today because you're hesitating too much!")

        cash = apple_portfolio.cash
        shares_hold = apple_portfolio.shares

    # After the trading process, calculate final portfolio value
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
