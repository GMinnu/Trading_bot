Binance Futures Testnet Trading Bot

This is a beginner-friendly Python trading bot for Binance Futures Testnet (USDT-M) built using the official python-binance library. The bot allows placing various types of orders on the Binance Futures Testnet with command-line input, robust validation, error handling, and comprehensive logging for easy monitoring and debugging.

Features :-
Connects securely to Binance Futures Testnet using user-provided API credentials.
Supports placing both Buy (Long) and Sell (Short) orders.
Handles multiple order types:
Market Orders — execute immediately at the market price.
Limit Orders — execute at a specified limit price.

Bonus Feature :-
Added support for Stop-Limit Orders, which combine a stop price trigger with a limit order.
Easy-to-use Command-Line Interface (CLI):
Menu-driven order type selection.
Prompts for all necessary order parameters.
Validates inputs for correctness.
Logs all API requests, responses, and errors to both console and a detailed log file (trading_bot.log).
Graceful error handling for API errors, network issues, and invalid user inputs.
Helps beginners learn how to interact with the Binance Futures API in a structured Python environment.

Getting Started

Prerequisites :-
Python 3.7 or higher
python-binance package (pip install python-binance)
Binance Futures Testnet API key and secret (obtain from https://testnet.binancefuture.com)

Running the Bot :-
Clone or download this repository.
Install required Python package:
pip install python-binance
Run the bot script:
python trading_bot.py

Enter your Binance Futures Testnet API Key and Secret.
Use the menu to select order types and enter trade details.
Check trading_bot.log for detailed logs and errors.

Additional Notes :-
This bot is intended for the Binance Futures Testnet environment only; do NOT use it with live API keys or real funds.
The flexible CLI allows easy extension for additional order types or features.
The built-in logging facilitates troubleshooting and audit of trading actions.
This project is ideal for demonstrating Python API integration, CLI interfaces, and basic trading automation skills.

Author
Satwik
