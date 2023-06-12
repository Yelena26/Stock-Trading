# ======================================================================================================
# Robinhood.py
# Author: Yelena Yu
# ======================================================================================================
#  Description:
#   Handle for Robinhood. Sends trade requests, queries order states and available assets.
# ======================================================================================================


import robin_stocks


class Robinhood:

    username = ""
    password = ""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def stocks(self, symbol, quantity, price):

        import robin_stocks as robin_stonks
        login = robin_stonks.login(self.username, self.password)

        # Buy stonks
        if quantity > 0:

            # Buy at market price.
            if price == "":
                robin_stonks.order_buy_market(symbol, quantity)

            # Buy at limit price.
            else:
                robin_stonks.order_buy_limit(symbol, quantity, price)

        # Sell stonks
        elif quantity < 0:

            # Sell at market price.
            if price == "":
                robin_stonks.order_sell_market(symbol, quantity)

            # Sell at limit price.
            else:
                robin_stonks.order_sell_limit(symbol, quantity, price)
