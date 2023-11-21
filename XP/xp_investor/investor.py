"""Investor helper."""
import csv
import re


def get_currency_rates_from_file(filename: str) -> tuple:
    """
    Read and return the currency and exchange rate history from file.

    See web page:
    https://www.eestipank.ee/valuutakursside-ajalugu

    Note that the return value is tuple, that consists of two things:
    1) currency name given in the file.
    2) exchange rate history for the given currency.
        Note that history is returned using dictionary where keys represent dates
        and values represent exchange rates for the dates.

    :param filename: file name to read CSV data from
    :return: Tuple that consists of currency name and dict with exchange rate history
    """
    regex_pattern = r'(?:\b(?:related to)\b\s+([A-Z]{3}))'
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        x = next(reader)[0].split(', {')
        currency = re.findall(regex_pattern, x[0])
        exchange_rates = {}
        y = next(reader)
        z = next(reader)
        for row in reader:
            exchange_rates[row[0]] = float(row[1])

    return currency[0], exchange_rates


def exchange_money(exchange_rates: dict) -> list:
    """
    Find best dates to exchange money for maximum profit.

    You are given a dictionary where keys represent dates and values represent exchange
    rates for the dates. The amount you initially have is 1000 and you always use the
    maximum amount during the exchange.
    Be aware that there is 1% of service fee for every exchange. You only need to return
    the dates where you take action. That means the first action is always to buy the
    second currency and the second action is to sell it back. Repeat the sequence as
    many times as you need for maximum profit. You should always end up having the
    initial currency. That means there should always be an even number of actions. You can
    also decide that the best decision is to not make any transactions at all, if
    for example the rate is always dropping. In that case just return an empty list.

    Initial amount of money 1000
    Service fee 1%
    :param exchange_rates: dictionary of dates and exchange rates
    :return: list of dates
    """
    dates_to_exchange = []
    initial_money = 1000
    current_money = initial_money
    service_fee = 0.99
    rates = list(exchange_rates.values())
    dropping_rates = sorted(rates, reverse=True)
    print(rates)
    print(dropping_rates)
    if dropping_rates == rates:
        return []




def best_day_to_buy(exchange_dict: dict) -> tuple:
    lowest_rate = min(exchange_dict.values())
    day_to_buy = ''
    for date, rate in exchange_dict.items():
        if rate <= lowest_rate:
            day_to_buy = date
            lowest_rate = rate
    return day_to_buy, lowest_rate


def best_day_to_sell(exchange_dict: dict) -> tuple:
    highest_rate = max(exchange_dict.values())
    day_to_buy = ''
    for date, rate in exchange_dict.items():
        if rate <= highest_rate:
            day_to_buy = date
            highest_rate = rate
    return day_to_buy, highest_rate



if __name__ == '__main__':
    data = get_currency_rates_from_file('data.txt')[1]
    print(data)

    print(exchange_money(data))