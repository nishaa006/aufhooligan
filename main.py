import logging
import pandas as pd
import json
from src.views import main_page
from src.reports import get_expenses_by_category
from src.services import load_operations_data, simple_search


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

raw_data = {
        "date": ["2025-01-15", "2025-02-20", "2025-03-10", "2025-03-25", "2025-04-05"],
        "category": ["Food", "Food", "Transport", "Food", "Food"],
        "amount": [100, 200, 50, 150, 100],
    }

date_str = "2025-04-10 15:30:00"


if __name__ == "__main__":
    response = main_page(date_str)
    print(json.dumps(response, indent=4, ensure_ascii=False))

    df = pd.DataFrame(raw_data)

    start_date = "2025-01-01"
    category = "Food"
    result = get_expenses_by_category(df, category, start_date)

    print(result)

    query1 = "транзакция 1"
    result_json = simple_search(query1, "../data/operations.xlsx")
    print(result_json)
