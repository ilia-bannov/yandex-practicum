import datetime as d
from datetime import datetime as dt
from decimal import Decimal


DATE_FORMAT = '%Y-%m-%d'

goods = {
    'Пельмени Универсальные': [
        {'amount': Decimal('0.5'), 'expiration_date': d.date(2024, 7, 1)},
        {'amount': Decimal('2'), 'expiration_date': d.date(2023, 8, 1)}
    ],
    'Вода': [{'amount': Decimal('1.5'), 'expiration_date': None}]
}


def add(items, title, amount, expiration_date=None):
    if expiration_date:
        expiration_date = dt.strptime(expiration_date, DATE_FORMAT).date()
    if title not in items:
        items[title] = []
    items[title].append({'amount': amount, 'expiration_date': expiration_date})


def add_by_note(items, note):
    parts = note.split(' ')
    # print(parts)
    if len(parts[-1].split('-')) == 3:
        expiration_date = parts[-1]
        amount = Decimal(str(parts[-2]))
        title = str.join(' ', parts[0:len(parts)-2])
    else:
        expiration_date = None
        amount = Decimal(str(parts[-1]))
        title = str.join(' ', parts[0:len(parts)-1])
    add(items, title, amount, expiration_date)


def find(items, needle):
    titles = []
    for title in items:
        if needle.lower() in title.lower():
            titles.append(title)
    return titles


def amount(items, needle):
    product_amount = Decimal('0')
    titles = find(items, needle)
    for title in titles:
        for item in items[title]:
            product_amount += item['amount']
    return product_amount


def expire(items, in_advance_days=0):
    products = list()
    expected_date = dt.today().date() + d.timedelta(days=in_advance_days)
    for title in items:
        product_amount = Decimal('0')
        for item in items[title]:
            exp_date = item['expiration_date']
            if exp_date is not None and exp_date <= expected_date:
                product_amount += item['amount']
        if product_amount > 0:
            products.append((title, product_amount))
    return products


add(goods, 'Яйца', Decimal('10'), '2024-07-01')
add(goods, 'Яйца', Decimal('3'), '2024-07-02')
add(goods, 'Вода', Decimal('2.5'))
add_by_note(goods, 'Яйца гусиные 4 2024-06-30')
add_by_note(goods, 'Яйца гусиные 5')
print(goods)
print(find(goods, 'А'))
print(amount(goods, 'яйца'))
print(amount(goods, 'морковь'))
print(expire(goods))
print(expire(goods, 1))
print(expire(goods, 2))
