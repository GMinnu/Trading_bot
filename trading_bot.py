import logging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import getpass

# Setup logging
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
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

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity,
            }
            if order_type == 'LIMIT':
                params["price"] = price
                params["timeInForce"] = TIME_IN_FORCE_GTC
            elif order_type == 'STOP_LIMIT':
                params["price"] = price
                params["stopPrice"] = stop_price
                params["timeInForce"] = TIME_IN_FORCE_GTC

            order = self.client.futures_create_order(**params)
            logging.info(f"Order placed: {order}")
            print(f"Order placed: {order['status']}")
        except BinanceAPIException as e:
            logging.error(f"BinanceAPI error: {e.message}")
            print(f"Binance error: {e.message}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print(f"Error: {e}")

def get_user_input():
    print("\nSelect order type:")
    print("1. Market")
    print("2. Limit")
    print("3. Stop-Limit")
    choice = input("Choice (1/2/3): ").strip()
    order_type = None
    if choice == '1':
        order_type = 'MARKET'
    elif choice == '2':
        order_type = 'LIMIT'
    elif choice == '3':
        order_type = 'STOP_LIMIT'
    else:
        print("Invalid choice, defaulting to Market order.")
        order_type = 'MARKET'

    symbol = input("Trade symbol (e.g., BTCUSDT): ").strip().upper()
    side = input("Side (BUY/SELL): ").strip().upper()
    while side not in ['BUY', 'SELL']:
        print("Side must be BUY or SELL.")
        side = input("Side (BUY/SELL): ").strip().upper()

    while True:
        try:
            quantity = float(input("Quantity: ").strip())
            if quantity <= 0:
                raise ValueError
            break
        except ValueError:
            print("Enter a positive number for quantity.")

    price = None
    stop_price = None
    if order_type == 'LIMIT':
        while True:
            try:
                price = float(input("Limit price: ").strip())
                if price <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Enter a positive number for limit price.")
    elif order_type == 'STOP_LIMIT':
        while True:
            try:
                stop_price = float(input("Stop price (trigger): ").strip())
                if stop_price <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Enter a positive number for stop price.")
        while True:
            try:
                price = float(input("Limit price: ").strip())
                if price <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Enter a positive number for limit price.")

    return symbol, side, order_type, quantity, price, stop_price

if __name__ == "__main__":
    print("=== Binance Futures Testnet Trading Bot ===")
    api_key = getpass.getpass("Enter Binance API Key (hidden): ")
    api_secret = getpass.getpass("Enter Binance API Secret (hidden): ")

    bot = BasicBot(api_key, api_secret)

    while True:
        symbol, side, order_type, quantity, price, stop_price = get_user_input()

        if not bot.symbol_exists(symbol):
            print(f"Symbol '{symbol}' is invalid or unsupported.")
            continue

        bot.place_order(symbol, side, order_type, quantity, price, stop_price)

        cont = input("Place another order? (y/n): ").strip().lower()
        if cont != 'y':
            break

    print("Exiting bot. Check trading_bot.log for details.")
