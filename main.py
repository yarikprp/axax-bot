import time
from datetime import datetime, timedelta

from bybit_service import create_exchange, get_market_data
from strategy import calculate_indicators, check_signal
from telegram_service import send_message
from onchain_service import check_onchain_activity
from logger import log_trade

from config import *


def main():

    send_message("🚀 Бот запущен")

    exchange = create_exchange()

    last_heartbeat = datetime.now()

    while True:

        try:

            # ❤️ heartbeat
            if datetime.now() - last_heartbeat > timedelta(hours=HEARTBEAT_INTERVAL_HOURS):

                send_message("❤️ Бот работает")

                last_heartbeat = datetime.now()

            # Получаем рынок
            df = get_market_data(exchange)

            latest = df.iloc[-1]

            print(
                f"Проверка {datetime.now()} | Price: {latest['close']} | OI: {latest['openInterest']} | Funding: {latest['fundingRate']}"
            )

            # --- защита от ошибок API ---
            if df is None or df.empty:

                print("⚠️ Market data not received")

                time.sleep(30)

                continue

            # индикаторы
            df = calculate_indicators(df)

            # сигнал
            signal = check_signal(df)

            if signal and check_onchain_activity():

                latest = df.iloc[-1]

                entry = latest["close"]

                if signal == "LONG":

                    stop = latest["low"]

                    risk = entry - stop

                    if risk <= 0:
                        continue

                    tp = entry + risk * RISK_REWARD_RATIO

                else:

                    stop = latest["high"]

                    risk = stop - entry

                    if risk <= 0:
                        continue

                    tp = entry - risk * RISK_REWARD_RATIO

                msg = f"""
🚨 SIGNAL {signal}

Entry: {entry:.3f}
SL: {stop:.3f}
TP: {tp:.3f}

Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

                send_message(msg)

                log_trade({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": signal,
                    "entry_price": entry,
                    "stop_loss": stop,
                    "take_profit": tp
                })

            time.sleep(CHECK_INTERVAL_SECONDS)

        except Exception as e:

            print("⚠️ Error:", e)

            send_message(f"⚠️ Error {e}")

            time.sleep(30)


if __name__ == "__main__":

    main()