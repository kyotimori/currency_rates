import unittest
import requests_mock
from currency_rates import get_currency_rate


class TestCurrencyRate(unittest.TestCase):
    def test_get_currency_rate(self):
        with requests_mock.Mocker() as m:
            m.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002',
                  text='''
                    <ValCurs Date="02.03.2002" name="Foreign Currency Market">
                    <Valute ID="R01235">
                    <NumCode>840</NumCode>
                    <CharCode>USD</CharCode>
                    <Nominal>1</Nominal>
                    <Name>Доллар США</Name>
                    <Value>31,01</Value>
                    </Valute>
                    </ValCurs>
                    ''')
            self.assertEqual(get_currency_rate('USD', '2002-03-02'), 'USD (Доллар США): 31,01')
            self.assertEqual(get_currency_rate('EUR', '2002-03-02'), 'Currency code EUR not found.')


if __name__ == '__main__':
    unittest.main()
