import requests
import pprint
import yaml
pp = pprint.PrettyPrinter(indent=4)

def import_portfolio(portfolio_name):
    """
    import the name of a portfolio file
    :param portfolio_name:
    :return:
    """

    file = open("portfolios/{portfolio_name}".format(portfolio_name=portfolio_name), "r")
    portfolio = yaml.load(file)

    return portfolio


def get_coin(symbol, market, exchange=None):
    """
    Look up a coin
    """
    r = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummary?market={market}-{symbol}'.format(
        market=market, symbol=symbol
    ))

    data = r.json()
    if data['result']:
        return data["result"][0]


def get_dollar_equivilant(btc_uds_value):

    one_dollar = btc_uds_value / 10000000

    return one_dollar



def collect_coin_data(coins):

    coin_data = {
        "coins": [],
        "usd_value": 0,
        "btc_value": 0,
        "coin_values": {
            "btc_usd": get_coin('btc', 'usdt')["Last"],
            "usd_btc": 1 / get_coin('btc', 'usdt')["Last"]
        }
    }

    for coin in coins:

        coin_row = {
            "usd": 0,
            "btc": 0,
            "symbol": "",
            "name": "",
            "qty": 0,
            "usd_total": 0,
            "btc_total": 0,
            "details": {"usd": None, "btc": None}
        }

        # get usd value
        usd_value = get_coin(coin['symbol'], 'usdt')
        # get btc value
        btc_value = get_coin(coin['symbol'], 'btc')
        if not usd_value:
            calculated_value = btc_value["Last"] / coin_data["coin_values"]["usd_btc"]
            usd_value = {"Last": calculated_value}

        coin_row["usd"] = usd_value["Last"]

        if coin["symbol"] == "btc":
            coin_row["btc"] = coin["qty"]
            coin_row["btc_total"] = coin["qty"]

        else:
            coin_row["btc"] = btc_value["Last"]
            coin_row["btc_total"] = coin["qty"] * btc_value["Last"]

        coin_row["name"] = coin["name"]
        coin_row["symbol"] = coin["symbol"]
        coin_row["qty"] = coin["qty"]
        coin_row["usd_total"] = coin["qty"] * usd_value["Last"]

        coin_data["coins"].append(coin_row)
        coin_data["usd_value"] += coin_row["usd_total"]
        coin_data["btc_value"] += coin_row["btc_total"]
    return coin_data



def print_data(coin_data, portfolio):

    print("=====================================================================")
    print("USD Investment: {0:.2f} - Profit: {1:.2f}".format(portfolio["usd_investment"], coin_data["usd_value"] - portfolio["usd_investment"]))
    print("USD Value: {0:.2f} - BTC Value: {1:.8f}".format(coin_data["usd_value"], coin_data['btc_value']))
    print("=====================================================================")
    for row in coin_data["coins"]:
        print("-----------------------------------------------------------------------------")
        print("{6}({0}) - BTC: {1:.8f} - USD: {2:.2f}\t|\tQTY: {3:.8f} - USD_TOTAL: {4:.2f} - BTC_TOTAL {5:8f}".format(
            row['symbol'].upper(),
            row['btc'],
            row['usd'],
            row['qty'],
            row['usd_total'],
            row['btc_total'],
            row['name']
            )
        )

    print("-----------------------------------------------------------------------------")
    bitcoin_value = get_coin("btc", 'usdt')["Last"]
    one_dollar_value = 1 / bitcoin_value
    print("1 USD = {0:.8f} Sats".format(one_dollar_value))
portfolio = import_portfolio("test.yml")

coin_data = collect_coin_data(portfolio["coins"])
print_data(coin_data, portfolio)
