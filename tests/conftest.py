import pytest
import pandas as pd
import os
import tempfile
import shutil

@pytest.fixture(scope="session")
def test_data_dir():
    """Crea directorio temporal para datos de prueba"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_csv_file(test_data_dir):
    """Crea archivo CSV de prueba"""
    csv_content = """fecha,producto,cantidad,precio_unitario
2024-01-01,ProductoA,10,100.0
2024-01-02,ProductoB,5,200.0
2024-01-03,ProductoA,15,100.0
2024-02-01,ProductoC,8,150.0
2024-02-02,ProductoB,12,200.0"""
    
    csv_path = os.path.join(test_data_dir, "test_ventas.csv")
    with open(csv_path, 'w') as f:
        f.write(csv_content)
    
    return csv_path

@pytest.fixture
def sample_invalid_csv_file(test_data_dir):
    """Crea archivo CSV con datos inválidos para testing"""
    csv_content = """fecha,producto,cantidad,precio_unitario
2024-01-01,ProductoA,10,100.0
2024-01-02,ProductoB,-5,200.0
invalid-date,ProductoC,8,150.0
2024-02-01,,12,200.0
2024-02-02,ProductoD,15,0"""
    
    csv_path = os.path.join(test_data_dir, "test_invalid_ventas.csv")
    with open(csv_path, 'w') as f:
        f.write(csv_content)
    
    return csv_path