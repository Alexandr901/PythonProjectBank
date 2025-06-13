import unittest
from pathlib import Path

from src.views import website


class TestWebsite(unittest.TestCase):
    def test_invalid_data_time(self):

        with self.assertRaises(TypeError):
            website("неверная дата")

    def test_file_existence(self):
        dir_transactions_excel = Path(__file__).parent.parent.resolve() / "data" / "operations.xlsx"
        self.assertTrue(dir_transactions_excel.exists())
