

class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.shares = 0
        self.total_invested = 0

    def buy(self, shares_to_buy, price):
        total_cost = shares_to_buy * price
        if total_cost <= self.cash:
            self.cash -= total_cost
            self.shares += shares_to_buy
            self.total_invested += total_cost
            print(f"Successfully bought {shares_to_buy} shares.")
        else:
            print("Transaction denied: not enough cash!")
        
    def sell(self, shares_to_sell, price):
        total_revenue = shares_to_sell * price
        if shares_to_sell <= self.shares:
            average_cost = self.average_cost()  # Get the average cost of the shares sold
            self.cash += total_revenue
            self.shares -= shares_to_sell
            self.total_invested -= shares_to_sell * average_cost
            print(f"Successfully sold {shares_to_sell} shares.")
        else:
            print("Transaction denied: not enough stock!")

    def hold(self):
        print("You chose to hold your position today.")

    def average_cost(self):
        if self.shares == 0:
            return 0
        return self.total_invested / self.shares