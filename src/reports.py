import json
import logging
from datetime import datetime, timedelta

import pandas as pd

logging.basicConfig(level=logging.INFO)


def get_expenses_by_category(df: pd.DataFrame, category: str, start_date: str) -> str:
    """Функция для получения отчета о тратах по категории за трехмесячный период."""
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = start_date + timedelta(days=90)
        df["date"] = pd.to_datetime(df["date"])
        logging.info(
            f"Данные отфильтрованы по категории: {category}, с {start_date.strftime('%Y-%m-%d')} по {end_date.strftime('%Y-%m-%d')}"
        )
        filtered_df = df[(df["category"] == category) & (df["date"] >= start_date) & (df["date"] <= end_date)]

        if filtered_df.empty:
            logging.warning("Нет данных для выбранной категории и периода.")
            return json.dumps({"error": "Нет данных для выбранной категории и периода."}, ensure_ascii=False, indent=4)
        category_expenses = filtered_df.groupby("category")["amount"].sum().reset_index()
        logging.info(
            f"Отчет по категории '{category}' за период с {start_date.strftime('%Y-%m-%d')} по {end_date.strftime('%Y-%m-%d')} успешно сформирован."
        )

        result = category_expenses.to_dict(orient="records")
        return json.dumps(result, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при формировании отчета: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    data = {
        "date": ["2025-01-15", "2025-02-20", "2025-03-10", "2025-03-25", "2025-04-05"],
        "category": ["Food", "Food", "Transport", "Food", "Food"],
        "amount": [100, 200, 50, 150, 100],
    }

    df = pd.DataFrame(data)

    start_date = "2025-01-01"
    category = "Food"
    result = get_expenses_by_category(df, category, start_date)

    print(result)
