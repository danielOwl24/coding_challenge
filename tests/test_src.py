import os
import yaml
import tempfile
from src.utils import load_queries, cast_dataframe
from src.models import * 
import pandas as pd
from src.models import *
from sqlalchemy.dialects.postgresql import insert
import yaml
import pytest
import numpy as np
from unittest.mock import MagicMock

def test_load_queries():
    sample_queries = {
        "get_departments": "SELECT * FROM departments;",
        "get_jobs": "SELECT * FROM jobs WHERE id = 1;"
    }

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as temp_file:
        yaml.dump(sample_queries, temp_file)
        temp_file_path = temp_file.name

    try:
        result = load_queries(temp_file_path)
        assert result == sample_queries

    finally:
        os.remove(temp_file_path)


@pytest.fixture
def sample_model():
    model = MagicMock()
    model.get_column_types_to_pandas.return_value = {
        "id": "int",
        "price": "float",
        "created_at": "datetime",
        "name": "string"
    }
    return model

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "id": [1, 2, 3, 4],
        "price": [10.5, 20.0, 23.4, np.nan],
        "created_at": ["2025-01-01", "2024-05-30", "2024-12-31", None],
        "name": ["Daniel", "Santiago", np.nan, "Fernando"]
    })

def test_cast_dataframe(sample_dataframe, sample_model):
    df = cast_dataframe(sample_dataframe, sample_model)
    assert df["id"].dtype == "Int64"  
    assert df["price"].dtype == "object"
    assert df["created_at"].dtype == "datetime64[ns]"
    assert df["name"].dtype == "object"
    
    assert df.loc[0, "id"] == 1
    assert df.loc[1, "price"] == 20.0
    assert pd.isna(df.loc[3, "created_at"])
    assert df.loc[2, "name"] is None
