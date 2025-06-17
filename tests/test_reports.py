import pandas as pd
import pytest

from src.reports import report_decorator_with_param, spending_by_category


def test_spending_by_category():
    transactions = pd.DataFrame(
        {
            "date": ["2025-06-01", "2025-05-15", "2025-04-10", "2025-03-20"],
            "category": ["food", "transport", "food", "entertainment"],
            "amount": [100, 50, 75, 200],
        }
    )
    transactions["date"] = pd.to_datetime(transactions["date"])
    category = "food"
    result = spending_by_category(transactions, category)
    expected = pd.DataFrame(
        {
            "date": ["2025-06-01", "2025-04-10"],
            "category": ["food", "food"],
            "amount": [100, 75],
        }
    )
    expected["date"] = pd.to_datetime(expected["date"])

    result = result.reset_index(drop=True)
    expected = expected.reset_index(drop=True)

    pd.testing.assert_frame_equal(result, expected)


@pytest.mark.parametrize("filename", ["report1.csv", "report2.csv"])
def test_report_decorator_with_param(filename):
    @report_decorator_with_param(filename)
    def func():
        return pd.DataFrame({"a": [1, 2], "b": [3, 4]})

    func()
    assert pd.read_csv(filename).equals(pd.DataFrame({"a": [1, 2], "b": [3, 4]}))
