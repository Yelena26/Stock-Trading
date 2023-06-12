# ======================================================================================================
# Simulator.py
# Author: Yelena Yu
# ======================================================================================================
#  Description:
#   Simulated brokerage account for paper trading and evaluating algorithm performance.
# ======================================================================================================


from rtstock.stock import Stock
import json


class Simulator:

    assets = {}

    def __init__(self, funds, assets=None):

        self.assets['$'] = float(funds)

        if assets is not None:
            self.assets = assets

    def get_portfolio_value(self, prices=None):
        value = self.assets['$']

        if prices is None:
            for symbol in self.assets:
                stonk = Stock(symbol)
                quote = stonk.get_latest_price()
                market_price = float(json.loads(quote)['LastTradePriceOnly'])
                value += market_price * self.assets[symbol]
        else:
            for symbol in self.assets:
                if symbol in prices:
                    market_price = prices[symbol]
                    value += market_price * self.assets[symbol]
                else:
                    stonk = Stock(symbol)
                    quote = stonk.get_latest_price()
                    market_price = float(json.loads(quote)['LastTradePriceOnly'])
                    value += market_price * self.assets[symbol]

        return value

    def stocks(self, symbol, quantity, price=-1):

        # Currently no way to simulate limit order transactions, so price is not used in simulator.
        # This parameter is left here to conform to the function definition interface.

        market_price = price
        if price < 0:
            stonk = Stock(symbol)
            quote = stonk.get_latest_price()
            market_price = float(json.loads(quote)['LastTradePriceOnly'])

        # Buy stonks
        if quantity > 0:
            if self.assets['$'] - market_price * quantity >= 0:
                self.assets['$'] -= (market_price * quantity)
                if symbol in self.assets:
                    self.assets[symbol] += quantity
                else:
                    self.assets[symbol] = quantity
                return 0
            return -1

        # Sell stonks
        elif quantity < 0:
            if symbol in self.assets and self.assets[symbol] >= -quantity:
                self.assets['$'] += (market_price * quantity)
                self.assets[symbol] += quantity
                return 0
            return -1
