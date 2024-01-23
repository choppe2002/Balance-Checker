import os
from dotenv import load_dotenv
import requests
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Load environment variables from .env file
load_dotenv()

# Retrieve Telegram API token, Etherscan API key, and BSCScan API key from environment variables
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY")

def get_ethereum_balance(wallet_address, etherscan_api_key):
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey={etherscan_api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        balance = int(data['result']) / 10**18
        return balance
    except requests.RequestException as e:
        print(f"Error fetching Ethereum balance: {e}")
        return None

def get_bsc_balance(wallet_address, bscscan_api_key):
    url = f'https://api.bscscan.com/api?module=account&action=balance&address={wallet_address}&apikey={bscscan_api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        balance = int(data['result']) / 10**18
        return balance
    except requests.RequestException as e:
        print(f"Error fetching BSC balance: {e}")
        return None

def handle_wallet_address(update, context):
    wallet_address = update.message.text

    print(f"Received wallet address: {wallet_address}")

    eth_balance = get_ethereum_balance(wallet_address, ETHERSCAN_API_KEY)
    bsc_balance = get_bsc_balance(wallet_address, BSCSCAN_API_KEY)

    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Ethereum Balance: {eth_balance or 0} ETH')
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'BSC Balance: {bsc_balance or 0} BNB')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to the Wallet Balance Checker Bot! Send me your wallet address to check the balances on Ethereum and BSC.')

def start_bot():
    # Check if TELEGRAM_API_TOKEN is set
    if TELEGRAM_API_TOKEN is None:
        print("Error: Telegram API Token is not set. Please check your .env file.")
        return

    updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_wallet_address))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    start_bot()
