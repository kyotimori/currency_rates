import requests
import click
import xml.etree.ElementTree as ET
import datetime


def validate_date(date):
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        raise ValueError('Неверный формат даты')
    return date


def format_date(date):
    date = date.split('-')
    date = '/'.join(date[::-1])
    return date


@click.command()
@click.option('--code', help='код валюты в формате ISO 4217')
@click.option('--date', help='дата в формате YYYY-MM-DD')
def get_currency_rate(code, date):
    flag = False
    if not date:
        date = str(datetime.date.today())
    if not code:
        flag = True
        print('Укажите код валюты в формате ISO 4217.')
    date = validate_date(date)
    date = format_date(date)
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
    response = requests.get(url)
    root = ET.fromstring(response.content)

    for i in root.findall('Valute'):
        if i.find('CharCode').text == code:
            flag = True
            print(f'{code} ({i.find("Name").text}): {i.find("Value").text}')
    if not flag:
        print(f'Код валюты {code} не найден.')


if __name__ == '__main__':
    get_currency_rate()
