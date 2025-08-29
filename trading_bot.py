# Import needed libraries
import logging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import getpass

# Setup logging to both file and console
logging.basicConfig(
    filename='trading_bot.log',           # Log file name
    level=logging.INFO,                   # Log all INFO and above
    format='%(asctime)s %(levelname)s:%(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# Define our trading bot class
class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        # Connect to Binance Futures Testnet
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.client.API_URL = "https://testnet.binancefuture.com/fapi"
        logging.info("Connected to Binance Futures Testnet.")

    def symbol_exists(self, symbol):
        try:
            info = self.client.futures_exchange_info()
            symbols = [item['symbol'] for item in info['symbols']]
            return symbol in symbols
        except Exception as e:
            logging.error(f"Error checking symbol {symbol}: {e}")
            return False

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }
            if order_type == 'LIMIT':
                params["price"] = price
                params["timeInForce"] = TIME_IN_FORCE_GTC

            order = self.client.futures_create_order(**params)
            logging.info(f"Order placed: {order}")
            print(f"Order placed: {order['status']} at {order.get('avgPrice', order.get('price', 'N/A'))}")
        except BinanceAPIException as e:
            logging.error(f"Binance error: {e.message}")
            print(f"Binance error: {e.message}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print(f"Unexpected error: {e}")

def get_user_input():
    # Input and validate details
    symbol = input("Enter symbol to trade (e.g. BTCUSDT): ").strip().upper()
    while not symbol.isalnum():
        print("Invalid symbol.")
        symbol = input("Enter symbol to trade: ").strip().upper()

    side = input("Order side (BUY/SELL): ").strip().upper()
    while side not in ['BUY', 'SELL']:
        print("Side must be BUY or SELL.")
        side = input("Order side (BUY/SELL): ").strip().upper()

    order_type = input("Order type (MARKET/LIMIT): ").strip().upper()
    while order_type not in ['MARKET', 'LIMIT']:
        print("Order type must be MARKET or LIMIT.")
        order_type = input("Order type (MARKET/LIMIT): ").strip().upper()

    while True:
        try:
            quantity = float(input("Enter quantity: ").strip())
            if quantity <= 0:
                raise ValueError
            break
        except ValueError:
            print("Enter a positive number for quantity.")

    price = None
    if order_type == 'LIMIT':
        while True:
            try:
                price = float(input("Enter limit price: ").strip())
                if price <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Enter a positive number for price.")

    return symbol, side, order_type, quantity, price

# Main code execution
if __name__ == "__main__":
    print("== Simple Binance Futures Testnet Trading Bot ==")
    api_key = getpass.getpass("Enter Binance API Key (input hidden): ")
    api_secret = getpass.getpass("Enter Binance API Secret (input hidden): ")

    bot = BasicBot(api_key, api_secret)

    while True:
        symbol, side, order_type, quantity, price = get_user_input()

        if not bot.symbol_exists(symbol):
            print(f"Symbol '{symbol}' not found on Binance Futures Testnet.")
            logging.warning(f"Tried invalid symbol: {symbol}")
            continue

        bot.place_order(symbol, side, order_type, quantity, price)

        again = input("Place another order? (y/n): ").strip().lower()
        if again != 'y':
            break

    print("Done. All logs are in trading_bot.log file.")
