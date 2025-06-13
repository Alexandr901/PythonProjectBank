import datetime
import json
import logging
from pathlib import Path

from src.utils import day_time_now, exchange_rate, get_price_stocks, max_five_transactions, user_transactions

logging.basicConfig(level=logging.INFO)

current_dir = Path(__file__).parent.parent.resolve()
dir_transactions_excel = current_dir / "data" / "operations.xlsx"


def website(data_time: datetime) -> str:
    """
    Главная функция, принимающую на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ со следующими данными:
    """
    print(f"Входные данные: {data_time}")

    # Проверка типа аргумента
    if not isinstance(data_time, datetime.datetime):
        raise TypeError("Аргумент data_time должен быть типа datetime.datetime")

    logging.info("Начинаем обработку данных...")

    result1 = day_time_now()
    result2 = user_transactions(data_time)
    result3 = max_five_transactions(data_time)
    result4 = exchange_rate()
    result5 = get_price_stocks()

    response = {
        "result1": result1,
        "result2": result2,
        "result3": result3,
        "result4": result4,
        "result5": result5,
    }

    return json.dumps(response)
