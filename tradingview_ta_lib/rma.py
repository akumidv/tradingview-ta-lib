import talib
import pandas as pd


def rma(src_ser, length):
    # src_ser = ta.verify_series(src_ser, length)
    alpha = 1/length
    sma = talib.SMA(src_ser, length)
    rma_val = [None] * src_ser.size
    for i in range(0, src_ser.size):
        if i == 0 or i < length:
            rma_val[i] = sma.iloc[i]
        else:
            rma_val[i] = alpha * src_ser.iloc[i] + (1 - alpha) * (rma_val[i-1] if rma_val[i-1] is not None else 0)
    rma_ser = pd.Series(data=rma_val, index=src_ser.index)
    return rma_ser

