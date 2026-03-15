import ccxt
import pandas as pd
from config import *


def create_exchange():

    exchange = ccxt.bybit({

        # защита от rate limit
        "enableRateLimit": True,

        # синхронизация времени
        "options": {
            "adjustForTimeDifference": True
        }
    })

    return exchange


def get_market_data(exchange):

    try:

        limit = PRICE_LOOKBACK_PERIOD + 10

        # свечи
        ohlcv = exchange.fetch_ohlcv(
            SYMBOL,
            TIMEFRAME,
            limit=limit
        )

        df = pd.DataFrame(
            ohlcv,
            columns=["timestamp", "open", "high", "low", "close", "volume"]
        )

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        # ---------- Open Interest ----------
        open_interest = 0
        try:
            oi = exchange.fetch_open_interest(SYMBOL)
            if oi:
                open_interest = oi.get("openInterestAmount", 0)
        except Exception as e:
            print("OI error:", e)

        # ---------- Funding Rate ----------
        funding_rate = 0
        try:
            fr = exchange.fetch_funding_rate(SYMBOL)
            if fr:
                funding_rate = fr.get("fundingRate", 0)
        except Exception as e:
            print("Funding error:", e)

        df["openInterest"] = open_interest
        df["fundingRate"] = funding_rate

        return df

    except Exception as e:

        print("Bybit data error:", e)

        return None