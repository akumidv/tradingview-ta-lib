import pandas as pd
import numpy as np
import atr


def hl2(high, low):
    """Indicator: HL2 """
    # Validate Arguments
    # high = verify_series(high)
    # low = verify_series(low)
    # offset = get_offset(offset)

    # Calculate Result
    hl2 = 0.5 * (high + low)

    # Name & Category
    hl2.name = "HL2"
    hl2.category = "overlap"

    return hl2


def supertrend(high_ser, low_ser, close_ser, length=None, multiplier=None):
    """Indicator: Supertrend"""
    # Validate Arguments
    length = int(length) if length and length > 0 else 7
    multiplier = float(multiplier) if multiplier and multiplier > 0 else 3.0
    # high_ser = ta.verify_series(high_ser, length)
    # low_ser = ta.verify_series(low_ser, length)
    # close_ser = ta.verify_series(close_ser, length)
    # offset = ta.get_offset(offset)
    if high_ser is None or low_ser is None or close_ser is None: return

    # Calculate Results
    m = close_ser.size
    dir_ = [1] * m
    trend = [0] * m
    hl2_ser = hl2(high_ser, low_ser)

    atr_ser = atr(high_ser, low_ser, close_ser, length) # talib.ATR(high, low, close, length)     # atr = ta.atr(high, low, close, length)
    matr = multiplier * atr_ser
    upperband_ser = hl2_ser + matr
    lowerband_ser = hl2_ser - matr

    for i in range(1, m):
        lowerband = lowerband_ser.iloc[i]
        upperband = upperband_ser.iloc[i]
        lowerband_prev_src = lowerband_ser.iloc[i - 1]# if i != 0 else np.NaN
        lowerband_prev = 0 if np.isnan(lowerband_prev_src) else lowerband_prev_src
        upperband_prev_src = upperband_ser.iloc[i - 1]# if i != 0 else np.NaN
        upperband_prev = 0 if np.isnan(upperband_prev_src) else upperband_prev_src
        if np.isnan(upperband): #atr.iloc[i-1]:
            dir_[i] = 1
        else:
            close = close_ser.iloc[i]
            close_prev = close_ser.iloc[i - 1] #if i !=0 else close

            lowerband_ser.iloc[i] = lowerband = lowerband if np.isnan(lowerband_prev_src) or lowerband > lowerband_prev or close_prev < lowerband_prev else lowerband_prev
            upperband_ser.iloc[i] = upperband = upperband if np.isnan(upperband_prev_src) or upperband < upperband_prev or close_prev > upperband_prev else upperband_prev
            if np.isnan(trend[i - 1]) or trend[i - 1] == upperband_prev:
                dir_[i] = -1 if close > upperband else 1
            else:
                dir_[i] = 1 if close < lowerband else -1
        trend[i] = lowerband if dir_[i] == -1 else upperband

    # Prepare DataFrame to return
    _props = f"{length}_{multiplier}"
    df = pd.DataFrame({
            f"SUPERT_{_props}": trend,
            f"SUPERTd_{_props}": dir_,
            # f'ATR_{length}': atr_ser,
            # 'upperband_ser': upperband_ser,
            # 'lowerband_ser': lowerband_ser,
        }, index=close_ser.index)

    df.name = f"SUPERT_{_props}"
    # df.category = "overlap"

    return df