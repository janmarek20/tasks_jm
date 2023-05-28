"""Program builds a valuation service
 according to the given conditions."""

import csv
import unittest

# Functions definitions.
def get_total_price(price, quantity):
    return price * quantity

def get_avg_price(total_price, count):
    if count > 0:
        return total_price / count
    else:
        return 0.0

def get_ignored_products_count(total_products, top_priced_count):
    return max(0, total_products - top_priced_count)

# Read data from files

# Read data from currencies.csv file.
currencies = {}
with open('currencies.csv', 'r') as currencies_file:
    currencies_reader = csv.DictReader(currencies_file)
    for row in currencies_reader:
        currency = row['currency']
        ratio = float(row['ratio'])
        currencies[currency] = ratio

# Read data from data.csv file.
products = []
with open('data.csv', 'r') as products_file:
    products_reader = csv.DictReader(products_file)
    for row in products_reader:
        product = {
            'id': int(row['id']),
            'price': float(row['price']),
            'currency': row['currency'],
            'quantity': int(row['quantity']),
            'matching_id': int(row['matching_id'])
        }
        products.append(product)

# Read data from matchings.csv file.
matchings = []
with open('matchings.csv', 'r') as matchings_file:
    matchings_reader = csv.DictReader(matchings_file)
    for row in matchings_reader:
        matching = {
            'matching_id': int(row['matching_id']),
            'top_priced_count': int(row['top_priced_count'])
        }
        matchings.append(matching)

# Conversion currency values into PLN
for product in products:
    currency = product['currency']
    ratio = currencies.get(currency, 1)
    product['price'] *= ratio

# Valuation for each match
results = []
for matching in matchings:
    matching_id = matching['matching_id']
    top_priced_count = matching['top_priced_count']

    matching_products = [p for p in products if p['matching_id'] == matching_id]
    matching_products = sorted(matching_products, key=lambda p: p['price'] * p['quantity'], reverse=True)
    top_products = matching_products[:top_priced_count]

    total_price = sum(p['price'] * p['quantity'] for p in top_products)
    avg_price = total_price / top_priced_count if top_priced_count > 0 else 0

    # Conversion of results into PLN.
    for product in top_products:
        product['price'] /= currencies[product['currency']]
        product['currency'] = 'PLN'

    currency = top_products[0]['currency'] if top_products else ''
    ignored_products_count = len(matching_products) - top_priced_count

    result = {
        'matching_id': matching_id,
        'total_price': total_price,
        'avg_price': avg_price,
        'currency': currency,
        'ignored_products_count': ignored_products_count
    }
    results.append(result)

# Save results to top_products.csv
fieldnames = ['matching_id', 'total_price', 'avg_price', 'currency', 'ignored_products_count']
with open('top_products.csv', 'w', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("Results are saved in file top_products.csv.")

# Unit tests


class EvaluationTests(unittest.TestCase):
    def test_total_price(self):
        self.assertEqual(get_total_price(2000, 1), 2000)
        self.assertEqual(get_total_price(1400, 3), 4200)
        self.assertEqual(get_total_price(0, 0), 0)

    def test_avg_price(self):
        self.assertEqual(get_avg_price(6000, 3), 2000)
        self.assertEqual(get_avg_price(4200, 5), 840)
        self.assertEqual(get_avg_price(0, 0), 0)

    def test_ignored_products_count(self):
        self.assertEqual(get_ignored_products_count(10, 7), 3)
        self.assertEqual(get_ignored_products_count(5, 5), 0)
        self.assertEqual(get_ignored_products_count(0, 10), 0)

if __name__ == '__main__':
    unittest.main()