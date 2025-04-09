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

        df = load_operations_data(file_path)

        results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]

        logger.info(f"Найдено {len(results)} транзакций по запросу: {query}")

        result_json = json.dumps({
            "query": query,
            "results_count": len(results),
            "results": results.to_dict(orient="records")
        }, ensure_ascii=False)

        return result_json
    except Exception as e:
        logger.error(f"Ошибка при выполнении поиска: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


query = input(f"введите запрос для поиска: ")
result_json = simple_search(query, "../data/operations.xlsx")
print(result_json)
