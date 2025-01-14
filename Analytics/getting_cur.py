import requests
import pandas as pd
from xml.etree import ElementTree as ET

def fetch_exchange_rates(start_year, end_year, currencies):
    data = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            date_str = f'01/{month:02}/{year}'
            rates = {'date': date_str}
            for currency in currencies:
                rate = get_exchange_rate(date_str, currency)
                if rate:
                    rates[currency] = rate
            data.append(rates)
    return pd.DataFrame(data)

def get_exchange_rate(date: str, currency: str) -> float:
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
    response = requests.get(url)
    root = ET.fromstring(response.content)
    for valute in root.findall('Valute'):
        char_code = valute.find('CharCode').text
        if char_code == currency:
            value = valute.find('Value').text.replace(',', '.')
            nominal = int(valute.find('Nominal').text)
            return float(value) / nominal
    return None

# Пример использования
currencies = ['BYR', 'EUR', 'KZT', 'UAH', 'USD']
df = fetch_exchange_rates(2003, 2025, currencies)
df.to_csv('exchange_rates.csv', index=False)
