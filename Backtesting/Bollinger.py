import pandas as pd
from typing import Tuple
from backtesting.test import GOOG

from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.lib import SignalStrategy


GOOG.tail()


def bollinger_bands(series, length: int = 20, *, num_stds: Tuple[float, ...] = (2, 0, -2), prefix: str = 'up') -> pd.Series:
    # Ref: https://stackoverflow.com/a/74283044/
    series = pd.Series(series)
    rolling = series.rolling(length)
    bband0 = rolling.mean()
    bband_std = rolling.std(ddof=0)
    #return pd.DataFrame({f'{prefix}{num_std}': (bband0 + (bband_std * num_std)) for num_std in num_stds})
    if prefix == 'up':
        return bband0 + (bband_std * num_stds[0])
    elif prefix == 'lower':
        return bband0 + (bband_std * num_stds[2])
    elif prefix == 'center':
        return bband0


def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return pd.Series(values).rolling(n).mean()


class bb(Strategy):

    n1 = 20
    n2 = 20

    def init(self):

        self.bollinger_up = self.I(bollinger_bands, self.data.Close, length=10, prefix='up')
        self.bollinger_down = self.I(bollinger_bands, self.data.Close, length=10, prefix='lower')
        self.bollinger_center = self.I(bollinger_bands, self.data.Close, length=10, prefix='center')


    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.data.Close, self.bollinger_up): #and crossover(self.data.Close, self.sma2):
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.bollinger_down, self._data.Close): #and crossover(self.sma2, self.data.Close):
            self.position.close()
            self.sell()

# +
from backtesting import Backtest

bt = Backtest(GOOG, bb, cash=10_000, commission=.002)
stats = bt.run()
stats
