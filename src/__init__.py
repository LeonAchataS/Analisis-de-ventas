"""
Paquete de análisis de ventas.
"""
# Solo importar las clases principales, no el visualizer automáticamente
from .data_processor import DataProcessor
from .analyzer import SalesAnalyzer
from .database import DatabaseManager

__version__ = "1.0.0"
__author__ = "Sales Analytics Team"

__all__ = [
    "DataProcessor",
    "SalesAnalyzer", 
    "DatabaseManager",
]
