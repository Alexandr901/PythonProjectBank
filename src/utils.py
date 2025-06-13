import json
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

from src.config import API_KEY_exchange, API_KEY_stocks

load_dotenv("../.env")

current_dir = Path(__file__).parent.parent.resolve()
dir_transactions_excel = current_dir / "data" / "operations.xlsx"
print(dir_transactions_excel)

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def day_time_now():
    """
    Функция, которая приветствует в зависимости от текущего времени суток.
    Использует логирование и возвращает JSON-ответ с приветствием.
    """

    try:
        current_date_time = datetime.datetime.now()
        hour = current_date_time.hour

        if 0 <= hour < 6 or 22 <= hour <= 23:
            greeting = "Доброй ночи"
        elif 17 <= hour <= 22:
            greeting = "Добрый вечер"
        elif 7 <= hour <= 11:
            greeting = "Доброе утро"
        else:
            greeting = "Добрый день"

        response = {
            "greeting": greeting,
            "current_time": current_date_time.strftime("%H:%M:%S"),
            "status": "success",
        }

        logging.info(f"Generated greeting: {greeting} at {current_date_time}")

        return json.dumps(response)

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return json.dumps(
            {
                "status": "error",
                "message": "Произошла ошибка при определении времени суток",
            }
        )


def user_transactions(data_time: pd.Timestamp) -> str:
    """
    Функция, которая извлекает детали транзакций для каждой карты:
    - последние 4 цифры карты
    - общие расходы
    - кэшбек (1 рубль за каждые 100 рублей расхода)

    Возвращает результат в формате JSON
    """

    try:
        df = pd.read_excel(dir_transactions_excel)

        df_filtered = df.loc[
            (pd.to_datetime(df["Дата операции"], dayfirst=True) <= data_time)
            & (pd.to_datetime(df["Дата операции"], dayfirst=True) >= data_time.replace(day=1))
        ].copy()

        df_filtered.loc[:, "кэшбек"] = df_filtered["Сумма операции с округлением"] // 100

        sales_by_card = df_filtered.groupby("Номер карты")[["Сумма операции с округлением", "кэшбек"]].sum()

        sorted_sales = sales_by_card.sort_values(by="Сумма операции с округлением", ascending=False)

        result = {
            "timestamp": datetime.now().isoformat(),
            "transactions": {
                card: {
                    "last_4_digits": str(card)[-4:],
                    "total_spent": float(sorted_sales.loc[card, "Сумма операции с округлением"]),
                    "cashback": float(sorted_sales.loc[card, "кэшбек"]),
                }
                for card in sorted_sales.index
            },
        }

        logging.info(f"Транзакции за период {data_time.strftime('%Y-%m-%d')} обработаны успешно")
        return json.dumps(result, ensure_ascii=False)

    except Exception as e:
        logging.error(f"Ошибка при обработке транзакций: {str(e)}")
        return json.dumps(
            {
                "error": "Произошла ошибка при обработке транзакций",
                "timestamp": datetime.now().isoformat(),
            }
        )


def max_five_transactions(data_time: pd.Timestamp) -> str:
    """
    Функция, которая извлекает 5 лучших транзакций по сумме платежа.
    Возвращает результат в формате JSON
    """

    try:
        df = pd.read_excel(dir_transactions_excel)

        filtered_df = df.loc[
            (pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S", dayfirst=True) <= data_time)
            & (
                pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S", dayfirst=True)
                >= data_time.replace(day=1)
            )
        ].copy()

        top_transactions = filtered_df.sort_values(by="Сумма операции с округлением", ascending=False).head(5)

        result = {
            "timestamp": datetime.now().isoformat(),
            "top_transactions": [
                {
                    "номер_карты": row["Номер карты"],
                    "дата_операции": row["Дата операции"],
                    "сумма": float(row["Сумма операции с округлением"]),
                    "тип_операции": row["Тип операции"],
                }
                for _, row in top_transactions.iterrows()
            ],
        }

        logging.info(f"Топ-5 транзакций за период {data_time.strftime('%Y-%m-%d')} обработаны успешно")
        return json.dumps(result, ensure_ascii=False)

    except Exception as e:
        logging.error(f"Ошибка при обработке транзакций: {str(e)}")
        return json.dumps(
            {
                "error": "Произошла ошибка при обработке транзакций",
                "timestamp": datetime.now().isoformat(),
            }
        )


def exchange_rate() -> str:
    """
    Функция, которая извлекает курсы обмена для USD и EUR к RUB
    путем вызова внешнего API. Возвращает результат в формате JSON.
    """

    try:
        currency_list = ["USD", "EUR"]
        convert_to = "RUB"
        rates = {}

        for currency in currency_list:
            url = f"https://api.apilayer.com/currency_data/convert?to={convert_to}&from={currency}&amount=1"
            headers = {"apikey": API_KEY_exchange}

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            rate = data.get("result")

            if rate is not None:
                rates[currency] = rate
                logging.info(f"Получен курс {currency} к RUB: {rate}")
            else:
                logging.error(f"Ошибка: ключ 'result' не найден в ответе для: {currency}")

        result = {
            "timestamp": datetime.now().isoformat(),
            "rates": rates,
            "status": "success",
        }

        return json.dumps(result, ensure_ascii=False)

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к API: {str(e)}")
        return json.dumps(
            {
                "error": "Произошла ошибка при получении курсов валют",
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
        return json.dumps(
            {
                "error": "Произошла непредвиденная ошибка",
                "timestamp": datetime.now().isoformat(),
            }
        )


def get_price_stocks() -> list:
    """
    Функция, которая извлекает цены акций из списка S&P 500
    путем вызова внешнего API.
    """
    stocks_list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    price_stocks = []

    for stock in stocks_list:
        response = requests.get(f"https://api.twelvedata.com/price?symbol={stock}&apikey={API_KEY_stocks}")
        dict_result = response.json()
        price_element = dict_result.get("price")
        price_stocks.append(price_element)

    return price_stocks
