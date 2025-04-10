import logging
import requests
from datetime import datetime
import pandas as pd
import json
import os
from dotenv import load_dotenv


load_dotenv()
api_url = os.getenv("API_URL")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_datetime(date_str: str) -> datetime:
    """Преобразует строку даты и времени в объект datetime."""
    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        logger.info(f"Дата успешно распознана: {parsed_date}")
        return parsed_date
    except ValueError as error:
        logger.error(f"Ошибка при разборе даты: {error}")
        raise


def fetch_data_from_api(date: datetime) -> list[dict]:
    """Имитация получения данных с API на заданную дату."""
    try:
        logger.info(f"Получение данных с API на дату: {date.date()}")
        mock_data = [
            {"value": 100, "date": str(date.date())},
            {"value": 150, "date": str(date.date())},
            {"value": 200, "date": str(date.date())},
        ]
        return mock_data
    except Exception as error:
        logger.error(f"Ошибка API-запроса: {error}")
        raise


def analyze_data(data: list[dict]) -> dict:
    """Анализирует данные, рассчитывая среднее значение и количество записей."""
    try:
        df = pd.DataFrame(data)
        logger.info("Данные успешно преобразованы в DataFrame")

        if "value" in df.columns:
            average = df["value"].mean()
        else:
            average = None
            logger.warning("Колонка 'value' отсутствует в данных")

        return {"average_value": average, "records_count": len(df)}
    except Exception as error:
        logger.error(f"Ошибка анализа данных: {error}")
        raise


def load_operations_data(filepath: str) -> pd.DataFrame:
    """Загружает данные из Excel-файла и возвращает DataFrame."""
    try:
        logger.info(f"Чтение Excel-файла: {filepath}")
        df = pd.read_excel(filepath)

        if "Дата операции" not in df.columns:
            logger.error("Колонка 'Дата операции' не найдена в Excel-файле")
            raise ValueError("Ожидаемая колонка 'Дата операции' отсутствует")

        return df
    except Exception as error:
        logger.error(f"Ошибка загрузки данных: {error}")
        raise


def get_current_date_from_api() -> str:
    """Получает текущую дату из внешнего API."""

    try:
        # Отправляем GET-запрос
        response = requests.get(api_url)

        # Проверка успешности запроса
        if response.status_code == 200:
            # Получаем данные в формате JSON
            date_data = response.json()

            # Логируем весь ответ для отладки
            logger.info(f"Ответ от API: {json.dumps(date_data, indent=4)}")

            # Попробуем извлечь дату, посмотрим на структуру ответа
            current_date = date_data.get("date", "Не удалось получить дату")

            return current_date
        else:
            logger.error(f"Ошибка при запросе данных: {response.status_code}")
            return "Ошибка при запросе данных"
    except Exception as e:
        logger.error(f"Произошла ошибка при получении даты: {e}")
        return "Ошибка при подключении к API"


# Пример вызова функции для получения текущей даты
if __name__ == "__main__":
    current_date = get_current_date_from_api()
    print(f"Текущая дата из API: {current_date}")
