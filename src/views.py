import logging
import json
from utils import load_operations_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def home_page(datetime_input):
    """Функция страницы «Главная»"""
    try:
        json_response = load_operations_data(datetime_input)
        return json.loads(json_response)
    except Exception as e:
        logger.error(f"Ошибка на главной странице: {e}")
        return {"error": "Ошибка обработки запроса"}
