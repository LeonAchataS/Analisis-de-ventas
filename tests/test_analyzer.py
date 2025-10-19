import pytest
import pandas as pd
from datetime import datetime
import sys
import os

# Agregar el directorio del proyecto al path para poder importar el paquete src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.data_processor import DataProcessor
from src.analyzer import SalesAnalyzer

class TestDataProcessor:
    
    def test_calculate_totals(self):
        """Test para validar cálculo de totales"""
        processor = DataProcessor()
        
        # Datos de prueba
        test_data = {
            'fecha': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'producto': ['ProductoA', 'ProductoB', 'ProductoC'],
            'cantidad': [10, 5, 8],
            'precio_unitario': [100.0, 200.0, 150.0]
        }
        
        processor.df = pd.DataFrame(test_data)
        result = processor.calculate_totals()
        
        # Verificar cálculos
        expected_totals = [1000.0, 1000.0, 1200.0]
        assert result['total'].tolist() == expected_totals
        
    def test_clean_data_removes_negative_quantities(self):
        """Test que verifica eliminación de cantidades negativas"""
        processor = DataProcessor()
        
        test_data = {
            'fecha': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'producto': ['ProductoA', 'ProductoB', 'ProductoC'],
            'cantidad': [10, -5, 8],
            'precio_unitario': [100.0, 200.0, 150.0]
        }
        
        processor.df = pd.DataFrame(test_data)
        result = processor.clean_data()
        
        # Debe quedar solo 2 filas (eliminó la cantidad negativa)
        assert len(result) == 2
        assert all(result['cantidad'] > 0)

class TestSalesAnalyzer:
    
    @pytest.fixture
    def sample_data(self):
        """Fixture con datos de prueba"""
        return pd.DataFrame({
            'fecha': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-02-01', '2024-02-02']),
            'producto': ['ProductoA', 'ProductoB', 'ProductoA', 'ProductoC'],
            'cantidad': [10, 5, 15, 8],
            'precio_unitario': [100.0, 200.0, 100.0, 150.0],
            'total': [1000.0, 1000.0, 1500.0, 1200.0]
        })
    
    def test_producto_mas_vendido(self, sample_data):
        """Test para producto más vendido por cantidad"""
        analyzer = SalesAnalyzer(sample_data)
        result = analyzer.producto_mas_vendido()
        
        # ProductoA tiene 25 unidades total (10+15)
        assert result['producto'] == 'ProductoA'
        assert result['cantidad_total'] == 25
    
    def test_producto_mayor_facturacion(self, sample_data):
        """Test para producto con mayor facturación"""
        analyzer = SalesAnalyzer(sample_data)
        result = analyzer.producto_mayor_facturacion()
        
        # ProductoA tiene $2500 total (1000+1500)
        assert result['producto'] == 'ProductoA'
        assert result['facturacion_total'] == 2500.0
    
    def test_facturacion_por_mes(self, sample_data):
        """Test para facturación mensual"""
        analyzer = SalesAnalyzer(sample_data)
        result = analyzer.facturacion_por_mes()
        
        # Verificar que hay 2 meses
        assert len(result) == 2
        
        # Enero: 1000 + 1000 = 2000
        # Febrero: 1500 + 1200 = 2700
        enero_key = list(result.keys())[0]
        febrero_key = list(result.keys())[1]
        
        assert result[enero_key] == 2000.0
        assert result[febrero_key] == 2700.0
    
    def test_get_top_productos_cantidad(self, sample_data):
        """Test para top productos por cantidad"""
        analyzer = SalesAnalyzer(sample_data)
        result = analyzer.get_top_productos_cantidad(2)
        
        # Debe retornar los 2 productos con más cantidad
        assert len(result) == 2
        assert 'ProductoA' in result
        assert result['ProductoA'] == 25