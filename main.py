# LIBRARIES AND FILES
import json
import time
import func_arbitrage

# VARIABLES
coin_price_url = "https://poloniex.com/public?command=returnTicker"

"""
    Step 0: finding coins which can be traded
    Exchange: Poloniex
    https://docs.poloniex.com/#introduction
    https://docs.legacy.poloniex.com/#introduction
"""
def step_0():

    # EXTRACT COIN PRICES FROM POLONIEX
    coin_json = func_arbitrage.get_coin_tickers(coin_price_url)

    # LOOP TO FIND TRADEABLE PAIRS
    coin_list = func_arbitrage.collect_tradeables(coin_json)

    return coin_list


"""
    Step 1: Structuring Triangular Pairs
    Calculations Only
"""
def step_1(coin_list):

    # STRUCTURE THE LIST OF TRIANGULAR PAIRS
    structured_list = func_arbitrage.structure_triangular_pairs(coin_list)

    # SAVE STRUCTURED LIST INTO JSON
    with open("structured_triangular_pairs.json", "w") as fp:
        json.dump(structured_list, fp)


"""
    Step 2: Calculating Surface Arbitrage Rates 
    Exchange: Poloniex
    https://docs.poloniex.com/#introduction
    https://docs.legacy.poloniex.com/#introduction
"""
def step_2():

    # GET STRUCTURED PAIRS
    with open("structured_triangular_pairs.json") as json.file:
        structured_pairs = json.load(json.file)

    # GET LATEST PRICES
    prices_json = func_arbitrage.get_coin_tickers(coin_price_url)

    # LOOP THROUGH AND STRUCTURE PRICE INFORMATION
    for t_pair in structured_pairs:
        time.sleep(0.3)
        prices_dict = func_arbitrage.get_prices_for_t_pair(t_pair, prices_json)
        surface_arb = func_arbitrage.calc_triangular_arb_surface_rate(t_pair, prices_dict)
        if len(surface_arb) > 0:
            real_rate_arb = func_arbitrage.get_depth_from_orderbook(surface_arb)
            print(real_rate_arb)
            time.sleep(20)

""" MAIN """
if __name__ == "__main__":
    # coin_list = step_0()
    # structured_pairs = step_1(coin_list)
    while True:
        step_2()
