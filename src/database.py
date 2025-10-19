import sqlite3
import pandas as pd
import json
from datetime import datetime
import os

class DatabaseManager:
    
    def __init__(self, db_path="output/database/ventas.db"):
        self.db_path = db_path
        self.ensure_directory()
        self.create_tables()
    
    def ensure_directory(self):
        """Crea directorio si no existe"""
        directory = os.path.dirname(self.db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    def get_connection(self):
        """Obtiene conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        """Crea las tablas necesarias"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla de ventas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha DATE,
                    producto TEXT,
                    cantidad INTEGER,
                    precio_unitario REAL,
                    total REAL
                )
            ''')
            
            # Tabla de resultados de análisis
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analisis_resultados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo_analisis TEXT,
                    resultado TEXT,
                    valor REAL,
                    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def insert_ventas_data(self, df):
        """Inserta datos de ventas desde DataFrame"""
        with self.get_connection() as conn:
            # Limpiar tabla existente
            conn.execute("DELETE FROM ventas")
            
            # Insertar nuevos datos
            df.to_sql('ventas', conn, if_exists='append', index=False)
            
        print(f"Insertadas {len(df)} filas en tabla ventas")
    
    def save_analysis_results(self, analysis_results):
        """Guarda resultados de análisis en BD"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Limpiar resultados anteriores
            cursor.execute("DELETE FROM analisis_resultados")
            
            # Guardar producto más vendido
            producto_vendido = analysis_results['producto_mas_vendido']
            cursor.execute('''
                INSERT INTO analisis_resultados (tipo_analisis, resultado, valor)
                VALUES (?, ?, ?)
            ''', ('producto_mas_vendido', producto_vendido['producto'], float(producto_vendido['cantidad_total'])))
            
            # Guardar producto mayor facturación
            producto_facturacion = analysis_results['producto_mayor_facturacion']
            cursor.execute('''
                INSERT INTO analisis_resultados (tipo_analisis, resultado, valor)
                VALUES (?, ?, ?)
            ''', ('producto_mayor_facturacion', producto_facturacion['producto'], float(producto_facturacion['facturacion_total'])))
            
            # Guardar top 3 productos por cantidad
            for i, (producto, cantidad) in enumerate(analysis_results['top_3_cantidad'].items(), 1):
                cursor.execute('''
                    INSERT INTO analisis_resultados (tipo_analisis, resultado, valor)
                    VALUES (?, ?, ?)
                ''', (f'top_3_cantidad_puesto_{i}', producto, float(cantidad)))
            
            conn.commit()
        
        print("Resultados de análisis guardados en BD")
    
    def get_top_productos_query(self, limit=3):
        """Consulta SQL para obtener top productos"""
        query = f'''
            SELECT producto, SUM(cantidad) as cantidad_total
            FROM ventas
            GROUP BY producto
            ORDER BY cantidad_total DESC
            LIMIT {limit}
        '''
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def get_facturacion_mensual_query(self):
        """Consulta SQL para facturación mensual"""
        query = '''
            SELECT strftime('%Y-%m', fecha) as mes, SUM(total) as facturacion_total
            FROM ventas
            GROUP BY strftime('%Y-%m', fecha)
            ORDER BY mes
        '''
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)