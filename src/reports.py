import json
import logging
import pandas as pd
import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_operations_data(file_path):
    """Загружает данные из Excel файла и возвращает их в формате DataFrame."""
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

def expenses_by_category(file_path, category, date_str):
    """Функция для получения отчета «Траты по категории» за трехмесячный период из файла Excel."""
    try:
        date_ref = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        start_date = date_ref - datetime.timedelta(days=90)
        end_date = date_ref

        df = load_operations_data(file_path)

        if 'Категория' not in df.columns or 'Дата платежа' not in df.columns or 'Сумма операции' not in df.columns:
            raise ValueError("Файл не содержит нужных столбцов ('Категория', 'Дата платежа', 'Сумма операции').")

        df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], dayfirst=True, errors='coerce')
        df['Сумма операции'] = df['Сумма операции'].replace(r'\s*RUB', '', regex=True)
        df['Сумма операции'] = pd.to_numeric(df['Сумма операции'], errors='coerce')

        filtered_df = df[(df['Категория'] == category) &
                         (df['Дата платежа'] >= start_date) &
                         (df['Дата платежа'] <= end_date)]

        total_expenses = filtered_df['Сумма операции'].abs().sum()

        result = {
            "category": category,
            "total_expenses": total_expenses,
            "period_start": start_date.date().isoformat(),
            "period_end": end_date.date().isoformat(),
        }

        logger.info(f"Общая сумма трат по категории '{category}' : {total_expenses}")
        return json.dumps(result, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Ошибка при расчете отчета: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

file_path = "../data/operations.xlsx"
category = input("Введите категорию: ").title()
date_str = input("Введите дату в формате YYYY-MM-DD: ")

result_json = expenses_by_category(file_path, category, date_str)

print(result_json)