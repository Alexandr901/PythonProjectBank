import json
import logging
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def filter_transactions(transactions):
    """
    Фильтрует транзакции, возвращая только те, которые относятся к переводам физлицам.

    """
    filtered_transactions = []
    for transaction in transactions:
        if transaction["category"] == "Переводы" and re.match(r"[А-Яа-я]+ [А-Я]\.", transaction["description"]):
            filtered_transactions.append(transaction)
    return filtered_transactions


def get_transactions():
    """
    Возвращает JSON со всеми транзакциями, которые относятся к переводам физлицам.

    """
    transactions = [
        {"id": 1, "category": "Переводы", "description": "Валерий А.", "amount": 1000},
        {
            "id": 2,
            "category": "Платежи",
            "description": "Оплата коммунальных услуг",
            "amount": 500,
        },
        {"id": 3, "category": "Переводы", "description": "Сергей З.", "amount": 2000},
        {"id": 4, "category": "Переводы", "description": "Артем П.", "amount": 1500},
    ]

    filtered_transactions = filter_transactions(transactions)
    logging.info(f"Отфильтровано {len(filtered_transactions)} транзакций")

    return json.dumps(filtered_transactions, ensure_ascii=False, indent=4)
