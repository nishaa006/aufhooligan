import pytest
import pandas as pd
import tempfile
import json
import os
from src.reports import expenses_by_category, load_operations_data


@pytest.fixture
def filled_excel_file():
    data = {
        "Категория": ["Еда", "Еда", "Транспорт", "Еда"],
        "Дата платежа": ["01.01.2024", "15.02.2024", "01.03.2024", "25.03.2024"],
        "Сумма операции": ["-500", "-300", "-200", "-100"]
    }
    df = pd.DataFrame(data)
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        yield tmp.name
        os.remove(tmp.name)

@pytest.fixture
def empty_excel_file():
    df = pd.DataFrame()
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        yield tmp.name
        os.remove(tmp.name)


def test_expenses_food(filled_excel_file):
    result_json = expenses_by_category(
        file_path=filled_excel_file,
        category="Еда",
        date_str="2024-03-31"
    )
    result = json.loads(result_json)
    assert result["category"] == "Еда"
    assert result["total_expenses"] == 900.0
    assert result["period_start"] == "2024-01-01"
    assert result["period_end"] == "2024-03-31"

def test_no_matching_category(filled_excel_file):
    result_json = expenses_by_category(
        file_path=filled_excel_file,
        category="Книги",
        date_str="2024-03-31"
    )
    result = json.loads(result_json)
    assert result["total_expenses"] == 0.0

def test_invalid_date_input(filled_excel_file):
    result_json = expenses_by_category(
        file_path=filled_excel_file,
        category="Еда",
        date_str="не-дата"
    )
    result = json.loads(result_json)
    assert "error" in result


def test_load_operations_success(filled_excel_file):
    df = load_operations_data(filled_excel_file)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert set(df.columns) == {"Категория", "Дата платежа", "Сумма операции"}


def test_load_operations_empty_file(empty_excel_file):
    with pytest.raises(ValueError, match="Файл пустой или не содержит данных"):
        load_operations_data(empty_excel_file)


def test_load_operations_file_not_found():
    with pytest.raises(Exception):
        load_operations_data("не_существующий_файл.xlsx")
