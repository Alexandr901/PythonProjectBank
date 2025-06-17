import logging
from typing import Optional

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).

    """
    if date is None:
        date = pd.Timestamp.now()
    else:
        date = pd.to_datetime(date)

    start_date = date - pd.DateOffset(months=3)
    filtered_transactions = transactions[(transactions["date"] >= start_date) & (transactions["date"] <= date)]

    category_transactions = filtered_transactions[filtered_transactions["category"] == category]

    return category_transactions


def report_decorator(func):
    """
    Декоратор для функций-отчетов, который записывает в файл результат, возвращаемый функцией.

    """

    def wrapper(*args, **kwargs):
        logging.info(f"Начало выполнения функции {func.__name__}")
        result = func(*args, **kwargs)
        with open("report.csv", "w") as file:
            result.to_csv(file, index=False)
        logging.info(f"Завершение выполнения функции {func.__name__}")
        return result

    return wrapper


def report_decorator_with_param(filename):
    """
    Декоратор с параметром для функций-отчетов, который принимает имя файла в качестве параметра.

    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            logging.info(f"Начало выполнения функции {func.__name__}")
            result = func(*args, **kwargs)
            with open(filename, "w") as file:
                result.to_csv(file, index=False)
            logging.info(f"Завершение выполнения функции {func.__name__}")
            return result

        return wrapper

    return decorator
