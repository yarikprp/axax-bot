from config import *

def calculate_indicators(df):

    df["rolling_low"] = df["low"].shift(1).rolling(PRICE_LOOKBACK_PERIOD).min()

    df["rolling_high"] = df["high"].shift(1).rolling(PRICE_LOOKBACK_PERIOD).max()

    df["oi_average"] = df["openInterest"].shift(1).rolling(OI_LOOKBACK_PERIOD).mean()

    return df


def check_signal(df):

    latest = df.iloc[-1]

    long_cond1 = latest["low"] < df["rolling_low"].iloc[-1] and latest["close"] > latest["open"]
    long_cond2 = latest["openInterest"] > df["oi_average"].iloc[-1]
    long_cond3 = latest["fundingRate"] <= MAX_FUNDING_RATE_FOR_LONG

    short_cond1 = latest["high"] > df["rolling_high"].iloc[-1] and latest["close"] < latest["open"]
    short_cond2 = latest["openInterest"] > df["oi_average"].iloc[-1]
    short_cond3 = latest["fundingRate"] >= MIN_FUNDING_RATE_FOR_SHORT

    if long_cond1 and long_cond2 and long_cond3:
        return "LONG"

    if short_cond1 and short_cond2 and short_cond3:
        return "SHORT"

    return None