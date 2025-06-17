import json
import unittest
from unittest import mock
from unittest.mock import patch

import pandas as pd

from src.utils import day_time_now, exchange_rate, get_price_stocks, max_five_transactions, user_transactions


class TestDayTimeNow(unittest.TestCase):
    @patch("datetime.datetime")
    def test_day_time(self, mocked_datetime):
        mocked_datetime.now.side_effect = Exception("Simulated error")

        result = day_time_now()

        expected_result = {"status": "error", "message": "Произошла ошибка при определении времени суток"}
        self.assertEqual(json.loads(result), expected_result)


@mock.patch("requests.get")
def test_get_price_stocks(mock_requests_get):
    stock_prices = [
        {"price": "232.62000"},
        {"price": "232.75999"},
        {"price": "185.32001"},
        {"price": "411.44000"},
        {"price": "328.5"},
    ]

    mock_requests_get.side_effect = [
        mock.Mock(json=lambda: stock_prices[0]),
        mock.Mock(json=lambda: stock_prices[1]),
        mock.Mock(json=lambda: stock_prices[2]),
        mock.Mock(json=lambda: stock_prices[3]),
        mock.Mock(json=lambda: stock_prices[4]),
    ]

    result = get_price_stocks()
    expected = ["232.62000", "232.75999", "185.32001", "411.44000", "328.5"]

    assert result == expected


class TestUserTransactions(unittest.TestCase):
    @patch("pandas.read_excel")
    @patch("logging.error")
    def test_user_transactions(self, mock_error, mock_read_excel):

        mock_read_excel.side_effect = Exception("Ошибка чтения файла")

        test_timestamp = pd.Timestamp("2025-06-15")

        result = user_transactions(test_timestamp)

        self.assertIn("error", json.loads(result))

        mock_error.assert_called_once_with("Ошибка при обработке транзакций: Ошибка чтения файла")


class TestMaxFiveTransactions(unittest.TestCase):
    @patch("pandas.read_excel")
    @patch("logging.info")
    @patch("logging.error")
    def test_max_five_transactions(self, mock_error, mock_info, mock_read_excel):
        test_data = {
            "Номер карты": [1234567890123456, 9876543210987654, 1111222233334444, 5555666677778888],
            "Дата операции": [
                "01.06.2025 10:00:00",
                "02.06.2025 14:00:00",
                "03.06.2025 16:00:00",
                "04.06.2025 18:00:00",
            ],
            "Сумма операции с округлением": [10000, 5000, 15000, 8000],
            "Тип операции": ["Покупка", "Снятие", "Перевод", "Оплата"],
        }

        df = pd.DataFrame(test_data)

        mock_read_excel.return_value = df

        test_timestamp = pd.Timestamp("2025-06-15")

        result = max_five_transactions(test_timestamp)

        json.loads(result)
        expected_result = {
            "top_transactions": [
                {
                    "номер_карты": 1111222233334444,
                    "дата_операции": "03.06.2025 16:00:00",
                    "сумма": 15000.0,
                    "тип_операции": "Перевод",
                },
                {
                    "номер_карты": 1234567890123456,
                    "дата_операции": "01.06.2025 10:00:00",
                    "сумма": 10000.0,
                    "тип_операции": "Покупка",
                },
                {
                    "номер_карты": 5555666677778888,
                    "дата_операции": "04.06.2025 18:00:00",
                    "сумма": 8000.0,
                    "тип_операции": "Оплата",
                },
                {
                    "номер_карты": 9876543210987654,
                    "дата_операции": "02.06.2025 14:00:00",
                    "сумма": 5000.0,
                    "тип_операции": "Снятие",
                },
            ]
        }


def test_exchange_rate():

    mock_response = {"result": 1.2345}

    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status.return_value = None

        result = exchange_rate()

        assert json.loads(result)["rates"]["USD"] == mock_response["result"]
        assert mock_get.called
