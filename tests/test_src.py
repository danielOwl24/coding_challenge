import os
import yaml
import tempfile
from src.utils import load_queries
from src.models import * 
import pandas as pd
from src.models import *
from sqlalchemy.dialects.postgresql import insert
import numpy as np
import yaml

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