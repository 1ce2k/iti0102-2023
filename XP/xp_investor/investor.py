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
    service_fee = 1 - 0.01
    dates = list(exchange_rates.keys())
    # for i in range(len(dates) - 1):
    #     # date when to buy
    #     date_buy = dates[i]
    #     # amount after buying like exchange 1000 EUR to 1067 USD by rate 1.067
    #     amount_after_buying = current_money * exchange_rates[date_buy]
    #     # take servise fee 1% from 1067 USD it would be 1056.33 USD
    #     amount_after_buying = amount_after_buying * service_fee
    #     print("Days to buy and amount")
    #     print(date_buy, amount_after_buying)
    #
    #     for x in range(i, len(dates)):
    #         # day when to sell
    #         date_sell = dates[x]
    #         # amount after selling like exchange 1000 USD to 937.207 EUR by rate 1.067
    #         amount_after_selling = amount_after_buying / exchange_rates[date_sell]
    #         # take servise fee 1% from 937.207 EUR it would be 927.835 EUR
    #         amount_after_selling = amount_after_selling * service_fee
    #         print("Days to sell and amount")
    #         print(date_sell, amount_after_selling)
    #     print()

    # if amount_after_selling > current_money:
    #     dates_to_exchange.extend([date_buy, date_sell])
    day_to_buy = best_day_to_buy(exchange_rates)
    day_to_sell = best_day_to_sell(exchange_rates)
    print(day_to_buy, day_to_sell)

    after_buying = current_money * exchange_rates[day_to_buy[0]]
    after_buying_with_fee = after_buying * 0.99
    after_selling = after_buying_with_fee / exchange_rates[day_to_sell[0]]
    after_selling_with_fee = after_selling * 0.99

    if after_selling_with_fee >= initial_money:
        dates_to_exchange.append(day_to_buy[0])
        dates_to_exchange.append(day_to_sell[0])
    return dates_to_exchange

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
            lowest_rate = rate
    return day_to_buy, highest_rate



if __name__ == '__main__':
    data = get_currency_rates_from_file('data.txt')[1]
    print(data)

    print(exchange_money(data))