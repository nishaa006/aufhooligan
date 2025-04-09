import unittest
from unittest.mock import patch
import pandas as pd
import json
from src.services import load_operations_data, simple_search

class TestSearchFunctions(unittest.TestCase):

    @patch('pandas.read_excel')
    def test_load_operations_data(self, mock_read_excel):
        mock_df = pd.DataFrame({
            'Категория': ['Такси', 'Еда'],
            'Дата платежа': ['2021-08-26', '2021-09-26'],
            'Сумма операции': ['-100.00 RUB', '-200.00 RUB']
        })
        mock_read_excel.return_value = mock_df

        result = load_operations_data('test_file.xlsx')
        mock_read_excel.assert_called_once_with('test_file.xlsx')
        pd.testing.assert_frame_equal(result, mock_df)

    @patch('search.load_operations_data')
    def test_simple_search(self, mock_load_operations_data):
        mock_df = pd.DataFrame({
            'Категория': ['Такси', 'Еда', 'Такси'],
            'Дата платежа': ['2021-08-26', '2021-09-26', '2021-10-26'],
            'Сумма операции': ['-100.00 RUB', '-200.00 RUB', '-150.00 RUB']
        })
        mock_load_operations_data.return_value = mock_df

        result = simple_search('такси', 'test_file.xlsx')
        expected_result = {
            "query": "такси",
            "results_count": 2,
            "results": [
                {'Категория': 'Такси', 'Дата платежа': '2021-08-26', 'Сумма операции': '-100.00 RUB'},
                {'Категория': 'Такси', 'Дата платежа': '2021-10-26', 'Сумма операции': '-150.00 RUB'}
            ]
        }
        self.assertEqual(json.loads(result), expected_result)

    @patch('search.load_operations_data')
    def test_simple_search_no_results(self, mock_load_operations_data):
        mock_df = pd.DataFrame({
            'Категория': ['Еда', 'Одежда'],
            'Дата платежа': ['2021-09-26', '2021-10-26'],
            'Сумма операции': ['-200.00 RUB', '-300.00 RUB']
        })
        mock_load_operations_data.return_value = mock_df

        result = simple_search('такси', 'test_file.xlsx')
        expected_result = {
            "query": "такси",
            "results_count": 0,
            "results": []
        }
        self.assertEqual(json.loads(result), expected_result)

if __name__ == '__main__':
    unittest.main()
