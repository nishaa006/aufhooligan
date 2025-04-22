import json

from src.utils import parse_datetime, fetch_data_from_api, analyze_data



def main_page(date_str: str):
    """Функция для страницы 'Главная', принимает строку с датой и временем и возвращает JSON-ответ."""
    try:
        # Парсим строку с датой
        date = parse_datetime(date_str)

        # Получаем данные с API
        raw_data = fetch_data_from_api(date)

        # Анализируем данные
        analysis_result = analyze_data(raw_data)

        # Формируем JSON-ответ
        json_response = json.dumps(analysis_result)

        return json_response

    except Exception as e:

        error_response = json.dumps({"error": "Внутренняя ошибка сервера"})
        return error_response


# Пример вызова функции
if __name__ == "__main__":
    date_input = "2025-04-10 15:30:00"  # Пример даты и времени
    response = main_page(date_input)
    print(json.dumps(response, indent=4, ensure_ascii=False))
