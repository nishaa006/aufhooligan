import json
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def load_operations_data(file_path):
    """Загружает данные из Excel файла и возвращает их в формате DataFrame"""
    try:
        logger.info(f"Загрузка данных из файла: {file_path}")
        df = pd.read_excel(file_path)
        if df.empty:
            raise ValueError("Файл пустой или не содержит данных.")
        logger.info(f"Данные загружены успешно. Всего записей: {len(df)}")
        return df

    except Exception as e:
        logger.error(f"Ошибка при загрузке данных из файла: {e}")
        raise


def simple_search(query, file_path):
    """Функция для сервиса «Простой поиск»"""
    try:
        logger.info(f"Запрос для поиска: {query}")

        query = query.lower()

        # Загружаем данные из Excel
        df = load_operations_data(file_path)

        # Выводим первые несколько строк для отладки
        logger.info(f"Первые несколько строк данных: {df.head()}")

        # Преобразуем все строки в DataFrame к строковому типу и ищем совпадения
        results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)]

        logger.info(f"Найдено {len(results)} транзакций по запросу: {query}")

        result_json = json.dumps(
            {"query": query, "results_count": len(results), "results": results.to_dict(orient="records")},
            ensure_ascii=False,
        )

        return result_json
    except Exception as e:
        logger.error(f"Ошибка при выполнении поиска: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# Пример запроса
query1 = "транзакция 1"
result_json = simple_search(query1, "../data/operations.xlsx")
print(result_json)
