# ======================================================================================================
# Oracle.py
# Author: Yelena Yu
# ======================================================================================================
#  Description:
#   Makes transactional decisions based on financial data and indicators along with available funds and
#   equities. Returns symbol to buy/sell along with quantity.
# ======================================================================================================


from datetime import datetime


# ===================================================================================================
#  Oracle
#  Description: Oracle object used for making transactional decisions.
# ===================================================================================================
class Oracle:

    stock = ''
    last_action = {}

    # ===================================================================================================
    #  Function: Constructor
    #  Description: Creates Oracle object, initializes member variables.
    #  Inputs: None
    #  Output: Oracle object with initialized states.
    # ===================================================================================================
    def __init__(self, stock):
        self.stock = stock
        self.last_action = {'time': -1, 'symbol': '', 'quantity': 0, 'price': 0}

    # ===================================================================================================
    #  Function: ask
    #  Description: Makes transactional decisions based on provided data.
    #  Inputs: Data frame containing Bollinger indicators (data frame).
    #          Available assets (dictionary).
    #  Output: Transactional decision (symbol, quantity, buy/sell).
    # ===================================================================================================
    def ask(self, df_bollinger, assets):

        current_time_seconds = get_current_time_seconds()
        print("[" + df_bollinger['label'].iloc[-1] + "] " +
              "Lower: " + str(df_bollinger['lower'].iloc[-1]) + ", " +
              "Upper: " + str(df_bollinger['upper'].iloc[-1]) + ", " +
              "Average: " + str(df_bollinger['moving average'].iloc[-1]) + ", " +
              "Close: " + str(df_bollinger['close'].iloc[-1]))

        quantity = 0
        closing_price = df_bollinger['close'].iloc[-1]

        # If closing price crosses lower boundary, buy asset with ~10% of available funds
        # if no previous purchases were made or if the asset has dropped by at least 5%.
        if df_bollinger['close'].iloc[-1] <= df_bollinger['lower'].iloc[-1]:
            if self.last_action['time'] < 0 or (closing_price - self.last_action['price']) / self.last_action['price'] < -0.05:
                quantity = int(0.1*assets['$']/closing_price)

        # If closing price crosses upper boundary, sell asset worth at least ~10% of available funds
        # if no previous purchases were made or if the asset has increased by at least 5%.
        if df_bollinger['close'].iloc[-1] >= df_bollinger['upper'].iloc[-1]:
            if self.last_action['time'] < 0 or (closing_price - self.last_action['price']) / self.last_action['price'] > 0.05:
                quantity = max(assets[self.stock], int(0.1*assets['$']/closing_price))

        # Record transaction details for evaluating next transaction.
        self.last_action['time'] = current_time_seconds
        self.last_action['symbol'] = self.stock
        self.last_action['quantity'] = quantity
        self.last_action['price'] = closing_price

        return [self.stock, quantity]


# ===================================================================================================
#  Function: get_current_time_seconds
#  Description: Calculates current time in seconds.
#  Inputs: None
#  Output: Current time in seconds (int).
# ===================================================================================================
def get_current_time_seconds():
    time_components = datetime.now().strftime("%H:%M:%S").split(':')
    return int(time_components[0]) * 3600 + int(time_components[1]) * 60 + int(time_components[2])
