

class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.shares = 0

    def buy(self, shares_to_buy, price):
        total_cost = shares_to_buy * price
        if total_cost <= self.cash:
            self.cash -= total_cost
            self.shares += shares_to_buy
            print(f"Successfully bought {shares_to_buy} shares.")
        else:
            print("Transaction denied: not enough cash!")
        
    def sell(self, shares_to_sell, price):
        total_revenue = shares_to_sell * price
        if shares_to_sell <= self.shares:
            self.cash += total_revenue
            self.shares -= shares_to_sell
            print(f"Successfully sold {shares_to_sell} shares.")
        else:
            print("Transaction denied: not enough stock!")

    def hold(self):
        print("You chose to hold your position today.")
    
    def net_worth(self, current_price):
        return self.cash + self.shares * current_price