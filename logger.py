import csv
import os
from config import TRADE_HISTORY_FILE

def log_trade(data):

    file_exists = os.path.isfile(TRADE_HISTORY_FILE)

    with open(TRADE_HISTORY_FILE,"a",newline="",encoding="utf-8") as f:

        fields = ["timestamp","type","entry_price","stop_loss","take_profit"]

        writer = csv.DictWriter(f, fieldnames=fields)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)