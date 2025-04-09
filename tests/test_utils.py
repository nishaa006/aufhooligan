import unittest
from unittest.mock import patch, MagicMock
import datetime
import pandas as pd
from src.utils import parse_datetime, fetch_data_from_api, analyze_data, load_operations_data

class TestOperations(unittest.TestCase):

    @patch('datetime.datetime.strptime')
    def test_parse_datetime_success(self, mock_strptime):
        mock_strptime.return_value = datetime.datetime(2025, 4, 8, 12, 30, 0)
        date_str = "2025-04-08 12:30:00"

        result = parse_datetime(date_str)
        self.assertEqual(result, datetime.datetime(2025, 4, 8, 12, 30, 0))

    @patch('datetime.datetime.strptime')
    def test_parse_datetime_error(self, mock_strptime):
        mock_strptime.side_effect = ValueError("Invalid format")
        date_str = "2025-04-08"

        with self.assertRaises(ValueError):
            parse_datetime(date_str)

    @patch('your_module.fetch_data_from_api')
    def test_fetch_data_from_api(self, mock_fetch):
        mock_date = datetime.datetime(2025, 4, 8)
        expected_data = [
            {"value": 100, "date": "2025-04-08"},
            {"value": 150, "date": "2025-04-08"},
            {"value": 200, "date": "2025-04-08"}
        ]
        mock_fetch.return_value = expected_data

        result = fetch_data_from_api(mock_date)
        self.assertEqual(result, expected_data)

    def test_analyze_data_success(self):
        raw_data = [
            {"value": 100, "date": "2025-04-08"},
            {"value": 150, "date": "2025-04-08"},
            {"value": 200, "date": "2025-04-08"}
        ]
        expected_result = {
            "average_value": 150,
            "records_count": 3
        }

        result = analyze_data(raw_data)
        self.assertEqual(result, expected_result)

    def test_analyze_data_missing_column(self):
        raw_data = [
            {"date": "2025-04-08"},
            {"date": "2025-04-08"},
            {"date": "2025-04-08"}
        ]
        expected_result = {
            "average_value": None,
            "records_count": 3
        }

        result = analyze_data(raw_data)
        self.assertEqual(result, expected_result)

    @patch('pandas.read_excel')
    def test_load_operations_data_success(self, mock_read_excel):
        mock_df = pd.DataFrame({
            'Дата операции': ['2025-04-08', '2025-04-09'],
            'Сумма': [100, 150]
        })
        mock_read_excel.return_value = mock_df

        result = load_operations_data("operations.xlsx")
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertIn('Дата операции', result.columns)

    @patch('pandas.read_excel')
    def test_load_operations_data_error(self, mock_read_excel):
        mock_read_excel.side_effect = ValueError("Не найдена колонка 'Дата операции'")

        with self.assertRaises(ValueError):
            load_operations_data("operations.xlsx")
