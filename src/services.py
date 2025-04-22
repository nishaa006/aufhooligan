import json
import pandas as pd
from pandas import DataFrame

def load_operations_data(file_path: str) -> DataFrame:
    """Загружает данные из Excel файла и возвращает их в формате DataFrame"""
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            raise ValueError("Файл пустой или не содержит данных.")
        return df
    except Exception as e:
        raise


def simple_search(query: str, file_path: str) -> str:
    """Функция для сервиса «Простой поиск»"""
    try:
        query = query.lower()
        df = load_operations_data(file_path)

        results = df[df.apply(
            lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1
        )]

        result_json: str = json.dumps(
            {
                "query": query,
                "results_count": len(results),
                "results": results.to_dict(orient="records")
            },
            ensure_ascii=False,
        )

        return result_json
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# Пример вызова
query1: str = "транзакция 1"
result_json: str = simple_search(query1, "../data/operations.xlsx")
print(result_json)
