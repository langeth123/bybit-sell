from loguru import logger
from ccxt import bybit as Bybit
from threading import Thread
import traceback
import ccxt
from time import sleep, time


ACCOUNTS = [i.replace("\n", "") for i in open("accs.txt").readlines()]
PRICES = [2, 2.5] # MIN, MAX prices
PAIR = 'SUI/USDT' 
SLEEP_FAILED_DELAY = 3 # sleep time in seconds after failed action
SLEEP_CHECKING_DELAY = 0.05 # sleep time in seconds for waiting timestamp
TIMESTAMP = 1683059400 # timestamp for placing orders. Check https://www.epochconverter.com/
AMOUNT_TO_SELL = 2 # amount in tokens to sell
