# ======================================================================================================
# main.py
# Author: Yelena Yu
# ======================================================================================================
#  Description:
#   Main driver code. Fetches financial data from web servers, calculates financial indicators, call on
#   oracle to make transactional decisions, trigger trade transactions, maintain market-hours activity,
#   routes data to relevant components, keeps track of portfolio value over time.
#
#  Usage:
#   Configurations and API keys are extracted from local configuration file config.txt.
# ======================================================================================================


import configparser
from Simulator import Simulator
import Oracle
from Oracle import Oracle
import time
from IEXCloud import IEXCloud


def main():
    config = configparser.ConfigParser()
    config.read('config.txt')
    quotes = config.get("ANALYSIS", "quotes").split(',')
    trade_interval = int(config.get('TIME', 'trade_interval'))
    mode = config.get('TIME', 'mode')
    iex_cloud_token = config.get('IEX CLOUD', 'token')

    iex_cloud = IEXCloud(iex_cloud_token)

    if mode == "retrospect":
        iex_cloud.get_intraday_bollinger(quotes[0], visualize=True)

    elif mode == "live":
        portfolio_value = []
        broker = Simulator(10000, {'AAPL': 20})
        oracle = Oracle()
        current_time_seconds = Oracle.get_current_time_seconds()

        # Market hours: 6:30 PST (9:30 EST) to 13:00 PST (16:00 EST)
        while 23400 < current_time_seconds < 46800:
            df_bollinger = iex_cloud.get_intraday_bollinger(quotes[0], False)  # Get financial indicators.
            [symbol, quantity] = oracle.ask(df_bollinger, broker.assets)       # Consult the oracle.

            # Execute the oracle's instructions.
            if quantity > 0:  # Positive quantity means buy.
                broker.stocks(symbol, quantity, df_bollinger['close'].iloc[-1])
                print("Bought " + str(quantity) + " " + symbol + " at " + str(df_bollinger['close'].iloc[-1]))
            elif quantity < 0:  # Negative quantity means sell.
                broker.stocks(symbol, quantity, df_bollinger['close'].iloc[-1])
                print("Sold " + str(quantity) + " " + symbol + " at " + str(df_bollinger['close'].iloc[-1]))

            # Track portfolio value.
            prices = {symbol: df_bollinger['close'].iloc[-1]}
            portfolio_value.append(broker.get_portfolio_value(prices))
            print(str(current_time_seconds) + " Portfolio Value: $" + str(portfolio_value[len(portfolio_value) - 1]))
            print(portfolio_value)

            time.sleep(trade_interval)
            current_time_seconds = Oracle.get_current_time_seconds()


main()
