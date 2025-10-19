import pandas as pd
import numpy as np
from datetime import datetime

class DataProcessor:
    
    def __init__(self):
        self.df = None
    
    def load_data(self, file_path):
        """Carga datos desde archivo CSV"""
        try:
            self.df = pd.read_csv(file_path)
            return self.df
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        except Exception as e:
            raise Exception(f"Error al cargar datos: {str(e)}")
    
    def clean_data(self):
        """Limpia datos nulos e inconsistentes"""
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        initial_rows = len(self.df)
        
        # Eliminar filas con valores nulos
        self.df = self.df.dropna()
        
        # Convertir fecha a datetime
        self.df['fecha'] = pd.to_datetime(self.df['fecha'], errors='coerce')
        self.df = self.df.dropna(subset=['fecha'])
        
        # Filtrar cantidades negativas o cero
        self.df = self.df[self.df['cantidad'] > 0]
        
        # Filtrar precios negativos o cero
        self.df = self.df[self.df['precio_unitario'] > 0]
        
        # Eliminar productos vacíos
        self.df = self.df[self.df['producto'].str.strip() != '']
        
        final_rows = len(self.df)
        print(f"Filas eliminadas en limpieza: {initial_rows - final_rows}")
        
        return self.df
    
    def calculate_totals(self):
        """Calcula columna total = cantidad * precio_unitario"""
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        self.df['total'] = self.df['cantidad'] * self.df['precio_unitario']
        return self.df
    
    def get_clean_data(self):
        """Retorna datos limpios"""
        return self.df
    
    def save_clean_data(self, output_path):
        """Guarda datos limpios en CSV"""
        if self.df is None:
            raise ValueError("No hay datos para guardar")
        
        self.df.to_csv(output_path, index=False)
        print(f"Datos limpios guardados en: {output_path}")