import json
import logging
from datetime import datetime

from src.utils import day_time_now, exchange_rate, get_price_stocks, max_five_transactions, user_transactions

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    """
    Главная функция для запуска всех функциональностей проекта.
    """
    try:
        logging.info("Запуск основного модуля")

        # Получаем текущее время
        current_time = datetime.now()
        logging.info(f"Текущее время: {current_time}")

        # Получаем все результаты
        logging.info("Получение текущего времени и даты")
        current_datetime = day_time_now()

        logging.info("Получение пользовательских транзакций")
        user_trans = user_transactions(current_time)

        logging.info("Получение пяти максимальных транзакций")
        max_trans = max_five_transactions(current_time)

        logging.info("Получение курсов валют")
        exchange_rates = exchange_rate()

        logging.info("Получение цен акций")
        stock_prices = get_price_stocks()

        # Формируем итоговый результат
        result = {
            "current_datetime": current_datetime,
            "user_transactions": user_trans.to_dict(orient="records"),
            "max_transactions": max_trans.to_dict(orient="records"),
            "exchange_rates": exchange_rates,
            "stock_prices": stock_prices,
        }

        # Сохраняем результат в JSON
        with open("results.json", "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)

        logging.info("Результаты успешно сохранены в results.json")

    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    main()
