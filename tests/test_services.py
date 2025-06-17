import json
import re

from src.services import filter_transactions, get_transactions


def test_filter_transactions():
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
    assert len(filtered_transactions) == 3
    assert all(transaction["category"] == "Переводы" for transaction in filtered_transactions)
    assert all(re.search(r"[А-Яа-я]", transaction["description"]) for transaction in filtered_transactions)


def test_get_transactions():

    json_data = get_transactions()
    transactions = json.loads(json_data)
    assert isinstance(transactions, list)
    assert all(isinstance(transaction, dict) for transaction in transactions)
