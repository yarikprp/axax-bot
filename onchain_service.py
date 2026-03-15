import requests
from datetime import datetime, timedelta
from config import *

def check_onchain_activity():

    try:

        url = f"https://api.snowtrace.io/api?module=account&action=tokentx&contractaddress=0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7&page=1&offset=50&sort=desc&apikey={ETHERSCAN_API_KEY}"

        r = requests.get(url, timeout=10)
        data = r.json()

        if data["status"] == "1":

            for tx in data["result"]:

                value = int(tx["value"]) / 10**18
                tx_time = datetime.fromtimestamp(int(tx["timeStamp"]))

                if (
                    value >= TRANSACTION_THRESHOLD_AVAX
                    and datetime.now() - tx_time < timedelta(hours=ONCHAIN_LOOKBACK_HOURS)
                ):
                    return True

        return False

    except Exception as e:

        print("Onchain error:", e)

        return False