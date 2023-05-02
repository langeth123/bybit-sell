# Bybit seller

It is a little script for selling tokens on the first seconds when token launched

# Features

- **Placing SELL orders with N price and N token amount in N timestamp**

- **Closing all open orders on account**

- **Script supporting proxies**

### Settings

Check the settings.py file

~~~python
PRICES = [2, 2.5] # MIN, MAX prices
PAIR = 'SUI/USDT' 
SLEEP_FAILED_DELAY = 3 # sleep time in seconds after failed action
SLEEP_CHECKING_DELAY = 0.05 # sleep time in seconds for waiting timestamp
TIMESTAMP = 1683059400 # timestamp for placing orders. Check https://www.epochconverter.com/
AMOUNT_TO_SELL = 2 # amount in tokens to sell

~~~

To change work status, check main.py file
~~~python
"""
Task numbers
1 - Place order
2 - Cancel all orders

"""

if __name__ == "__main__":
    task_number = 1
    main()
