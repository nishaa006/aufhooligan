
import requests
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()
api_url = os.getenv("API_URL")


def parse_datetime(date_str: str) -> datetime:
    """Преобразует строку даты и времени в объект datetime."""
    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return parsed_date
    except ValueError as error:

        raise


def fetch_data_from_api(date: datetime) -> list[dict]:
    """Имитация получения данных с API на заданную дату."""
    try:

        mock_data = [
            {"value": 100, "date": str(date.date())},
            {"value": 150, "date": str(date.date())},
            {"value": 200, "date": str(date.date())},
        ]
        return mock_data
    except Exception as error:

        raise


def analyze_data(data: list[dict]) -> dict:
    """Анализирует данные, рассчитывая среднее значение и количество записей."""
    try:
        df = pd.DataFrame(data)


        if "value" in df.columns:
            average = df["value"].mean()
        else:
            average = None

        return {"average_value": average, "records_count": len(df)}
    except Exception as error:

        raise


def load_operations_data(filepath: str) -> pd.DataFrame:
    """Загружает данные из Excel-файла и возвращает DataFrame."""
    try:

        df = pd.read_excel(filepath)

        if "Дата операции" not in df.columns:

            raise ValueError("Ожидаемая колонка 'Дата операции' отсутствует")

        return df
    except Exception as error:

        raise


def get_current_date_from_api() -> str:
    """Получает текущую дату из внешнего API."""
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            date_data = response.json()

            current_date = date_data.get("date") or date_data.get("formatted")
            if current_date:
                return datetime.strptime(current_date, "%d/%m/%Y").strftime("%Y-%m-%d")
            return "Не удалось получить дату"
        else:

            return "Ошибка при запросе данных"
    except Exception as e:

        return "Ошибка при подключении к API"


if __name__ == "__main__":
    current_date = get_current_date_from_api()
    print(f"Текущая дата из API: {current_date}")
