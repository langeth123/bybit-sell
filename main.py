from settings import *

def account_session_handler(account_data: str) -> Bybit:
    api_key, secret_key, proxy = account_data.split(":", maxsplit=2)
    bybit = Bybit(
        {
            "apiKey": api_key,
            "secret": secret_key
        }
    )
    bybit.session.proxies.update(
        {
            "http": f'http://{proxy}',
            "https": f'http://{proxy}'
        }
    )
    return bybit


def prepare_accounts() -> dict:
    accs_amount = len(ACCOUNTS)
    prices_data, i, temp_price = [], 1, 0
    if accs_amount == 1:
        prices_data.append({"number": 1, "price": PRICES[0], "bybit": account_session_handler(ACCOUNTS[0])})

    elif accs_amount == 2:
        temp_price = PRICES[0]
        prices_data.append({"number": 1, "price": PRICES[0], "bybit": account_session_handler(ACCOUNTS[0])})
        prices_data.append({"number": 2, "price": PRICES[1], "bybit": account_session_handler(ACCOUNTS[1])})

    else:
        step = (PRICES[1] - PRICES[0]) / (accs_amount-1)
        for acc in ACCOUNTS:
            if i == 1:
                temp_price = PRICES[0]
            elif i == accs_amount:
                temp_price = PRICES[1]
            else:
                temp_price += step
            
            prices_data.append({"number": i, "price": round(temp_price, 3), "bybit": account_session_handler(acc)})
            i += 1
    
    for k in prices_data:
        logger.info(f"Account: #{k.get('number')} | Price: {k.get('price')}")
    

    """
    :return -> {"number": N, "price": N, "bybit": Bybit}
    """
    return prices_data
        
def process_sell(account_data: dict) -> None:
    number, price, bybit = account_data.values()
    logger.info(f'Account: #{number} | cancelling all orders and open active session with: {bybit.hostname}')
    remove_all_orders(account_data)

    while time() < TIMESTAMP:
        #logger.info("waiting")
        sleep(SLEEP_CHECKING_DELAY)
        pass

    logger.info(f'Account: #{number}, setting sell order for pair: {PAIR}, with price: {price}')
    while True:
        try:
            response = bybit.create_limit_sell_order(PAIR, AMOUNT_TO_SELL, price)
            if response.get("status") == 'open':
                logger.success(f'Account: #{number} | placed the order. Order id: {response.get("id")}')
                return
            else:
                logger.error(f'Account: #{number} | Failed order! Response: {response}')

        except Exception as error:
            if "Proxy" in str(traceback.format_exc()):
                logger.error(f'Account: #{number} | Failed because Proxy dead! | {error}')
            elif "Insufficient balance" in str(error):
                logger.error(f'Account: #{number} | Have insufficient balance for order')
            elif "bybit does not have market symbol" in str(error):
                pass
            else:
                logger.error(f'Account: #{number} | Failed with error: {error}')
        sleep(SLEEP_FAILED_DELAY)


def remove_all_orders(account_data: dict) -> None:
    number, _, bybit = account_data.values()
    try:
        response = bybit.cancel_all_spot_orders(PAIR)
        if response.get("ret_msg") == 'OK':
            logger.success(f'Account: #{number} | All orders was removed')
        else:
            logger.error(f'Account: #{number} | Cant cancel all orders! Response: {response}')
    except Exception as error:
        if "Proxy" in str(traceback.format_exc()):
            logger.error(f'Account: #{number} | Failed because Proxy dead! | {error}')
        else:
            logger.error(f'Account: #{number} | Failed with error: {error}')

def main() -> None:
    accounts_data = prepare_accounts()
    if task_number == 1:
        task = process_sell
    elif task_number == 2:
        task = remove_all_orders

    thread_list = [
        Thread(target=task, args=(acc,)) for acc in accounts_data
    ]

    for thread in thread_list:
        thread.start()



if __name__ == "__main__":
    task_number = 1
    main()
