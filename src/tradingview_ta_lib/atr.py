import talib
import pandas as pd
import rma


def tv_atr(high_ser, low_ser, close_ser, length):
    # high_ser = ta.verify_series(high_ser, length)
    # low_ser = ta.verify_series(low_ser, length)
    # close_ser = ta.verify_series(close_ser, length)
    tr = [None] * close_ser.size
    for i in range(0, close_ser.size): # TODO speed up by test talib or pandas-ta
        high = high_ser.iloc[i]
        low = low_ser.iloc[i]
        if i == 0:
            true_range = high - low
        else:
            close_prev = close_ser.iloc[i-1]
            true_range = max(max(high - low, abs(high - close_prev)), abs(low - close_prev))
        tr[i] = true_range  # ta.rma(true_range, length)
    tr_ser = pd.Series(data=tr, index=close_ser.index)
    atr_ser = rma(tr_ser, length)     # atr_ser = ta.rma(tr_ser, length)
    return atr_ser
