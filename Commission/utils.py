from datetime import date


LOCKS_PRICE = 45
STOCKS_PRICE = 30
BARRELS_PRICE = 25


def date_from_string(_str):
    year, month, day = _str.split('-')
    return date(int(year), int(month), int(day))


def get_available_goods(user, year, month):
    _sales = []
    target_date_start = date(int(year), int(month), 1)
    target_date_end = date(int(year), int(month + 1), 1)
    for sale in user.sales:
        if target_date_start < sale.date < target_date_end:
            _sales.append(sale)

    total_locks = 0
    total_stocks = 0
    total_barrels = 0
    for sale in _sales:
        total_locks += sale.locks
        total_stocks += sale.stocks
        total_barrels += sale.barrels
    return (total_locks, total_stocks, total_barrels)


def is_qualified_for_commission(total_locks, total_stocks, total_barrels):
    return total_locks == 0 or total_stocks == 0 or total_barrels == 0


def get_commission(total_locks, total_stocks, total_barrels):
    result = 0
    total_sales = total_locks * LOCKS_PRICE + total_stocks * \
        STOCKS_PRICE + total_barrels * BARRELS_PRICE
    if total_sales <= 1000:
        result = total_sales * 0.1
    elif total_sales > 1000 and total_sales <= 1800:
        result = 1000 * 0.1 + (total_sales - 1000) * 0.15
    elif total_sales > 1800:
        result = 1000 * 0.1 + 800 + 0.15 + (total_sales - 1800) * 0.2

    return result
