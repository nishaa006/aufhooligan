import logging
import datetime
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_datetime(date_str):
    """Преобразует строку с датой и временем в объект datetime"""
    try:
        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        logger.info(f"Успешный парсинг: {dt}")
        return dt
    except ValueError as e:
        logger.error(f"Ошибка парсинга даты: {e}")
        raise

def fetch_data_from_api(date):
    """Получает данные с внешнего API по дате"""
    try:
        logger.info(f"Запрос данных с API для даты: {date.date()}")
        # Для демонстрации: заглушка с данными
        data = [
            {"value": 100, "date": str(date.date())},
            {"value": 150, "date": str(date.date())},
            {"value": 200, "date": str(date.date())}
        ]
        return data
    except Exception as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        raise

def analyze_data(raw_data):
    """Обрабатывает данные с использованием pandas"""
    try:
        df = pd.DataFrame(raw_data)
        logger.info("Данные преобразованы в DataFrame")

        if 'value' in df.columns:
            avg = df['value'].mean()
        else:
            avg = None
            logger.warning("Колонка 'value' не найдена")

        return {
            "average_value": avg,
            "records_count": len(df)
        }
    except Exception as e:
        logger.error(f"Ошибка при анализе данных: {e}")
        raise

def load_operations_data(file_path):
    """Загружает данные из Excel файла и возвращает их в формате DataFrame"""
    try:
        logger.info(f"Загрузка данных из файла: {file_path}")
        df = pd.read_excel(file_path)

        if 'Дата операции' not in df.columns:
            logger.error("Не найдена колонка 'date' в файле.")
            raise ValueError("Не найдена колонка 'date' в файле.")

        return df
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных из файла: {e}")
        raise

result = load_operations_data("../data/operations.xlsx")
print(result)

