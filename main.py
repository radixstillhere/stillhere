
import requests
import time
from telegram import Bot

# === CONFIG ===
TOKEN_RESOURCE_ADDRESS = "resource_rdx1tkc3awevlsyxe6rg02a20kr9m3dhagkun8jcd9avqjufep4n9srsuu"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHANNEL = "@xrdSTILLHERE"

# === INIT ===
bot = Bot(token=TELEGRAM_BOT_TOKEN)
seen_tx_ids = set()

def get_latest_transactions():
    url = f"https://mainnet.radixdlt.com/transaction/committed?limit=20"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    return data.get("transactions", [])

def check_for_buys():
    txs = get_latest_transactions()
    for tx in txs:
        tx_id = tx.get("transaction_identifier", {}).get("hash")
        if not tx_id or tx_id in seen_tx_ids:
            continue
        seen_tx_ids.add(tx_id)

        state_updates = tx.get("affected_global_entities", [])
        if any(TOKEN_RESOURCE_ADDRESS in entity for entity in state_updates):
            message = f"💸 Buy Alert: $STILLHERE activity detected!\nTX Hash: {tx_id}\n#STILLHERE #Radix"
            bot.send_message(chat_id=TELEGRAM_CHANNEL, text=message)

def main_loop():
    print("Buy alert bot is running...")
    while True:
        try:
            check_for_buys()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(30)

if __name__ == "__main__":
    main_loop()
