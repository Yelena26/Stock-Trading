# ======================================================================================================
# AlphaVantage.py
# Author: Yelena Yu
# ======================================================================================================
#  Description:
#   Handle for interacting with Alpha Vantage web service and generating financial indicators to use by
#   other components. An Alpha Vantage account is required to obtain a key that must be included in all
#   Rest-based queries to the server. Data is returned in the form of JSON strings.
# ======================================================================================================


from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import collections


class AlphaVantage:

    api_key = ""

    def __init__(self, key):
        self.api_key = key

    def get_bollinger_bands(self, quote, start_time, end_time, resolution, visualize=False):
        ti = TechIndicators(key=self.api_key, output_format='pandas')
        bb_data, bb_m_data = ti.get_bbands(symbol=quote, interval=str(resolution)+'min')
        ts_data, ts_m_data = self.get_time_series(quote, start_time, end_time, resolution)

        if visualize:
            time_axis = []
            close = []
            counter = 0
            data = collections.OrderedDict(list(ts_data.items()))
            for key in data:
                if (counter >= 19):
                    time_axis.append(counter-19)
                    close.append(float(data[key]['4. close']))
                counter += 1

            fig, ax_bollinger = plt.subplots()
            ax_timeseries = ax_bollinger.twinx()
            bb_data.plot(ax=ax_bollinger)
            ax_timeseries.plot(bb_data.axes[0].values, close, ':r')
            plt.title('Bollinger Bands for ' + quote + ' (' + str(resolution) + ' min)')
            plt.show()

    def get_time_series(self, quote, start_time, end_time, resolution):
        ts = TimeSeries(key=self.api_key)
        return ts.get_intraday(symbol=quote, interval=str(resolution)+'min', outputsize='full')

