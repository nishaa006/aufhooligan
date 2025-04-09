import unittest
from unittest.mock import patch
import json
from src.views import home_page

class TestHomePage(unittest.TestCase):

    @patch('your_module.load_operations_data')
    def test_home_page_success(self, mock_load_operations_data):
        mock_datetime_input = '2025-04-08'
        mock_json_response = json.dumps({
            "data": [
                {"operation": "purchase", "amount": 100},
                {"operation": "refund", "amount": 50}
            ]
        })
        mock_load_operations_data.return_value = mock_json_response

        result = home_page(mock_datetime_input)
        expected_result = {
            "data": [
                {"operation": "purchase", "amount": 100},
                {"operation": "refund", "amount": 50}
            ]
        }

        self.assertEqual(result, expected_result)

    @patch('your_module.load_operations_data')
    def test_home_page_error(self, mock_load_operations_data):
        mock_datetime_input = '2025-04-08'
        mock_load_operations_data.side_effect = Exception("Ошибка в загрузке данных")

        result = home_page(mock_datetime_input)
        expected_result = {"error": "Ошибка обработки запроса"}

        self.assertEqual(result, expected_result)

