#!/usr/bin/env python3

import os
import sys
from src.data_processor import DataProcessor
from src.analyzer import SalesAnalyzer
from src.database import DatabaseManager

def main():
    """Script principal para análisis de ventas"""
    
    # Configuración de rutas
    input_file = "data/raw/ventas.csv"
    clean_file = "data/processed/ventas_clean.csv"
    
    print("=== ANÁLISIS DE VENTAS ===")
    
    try:
        # 1. Carga y limpieza de datos
        print("\n1. Cargando y limpiando datos...")
        processor = DataProcessor()
        
        if not os.path.exists(input_file):
            print(f"Error: Archivo {input_file} no encontrado")
            print("Por favor, coloca el archivo ventas.csv en la carpeta data/raw/")
            return
        
        # Crear directorio si no existe
        os.makedirs("data/processed", exist_ok=True)
        
        # Procesar datos
        processor.load_data(input_file)
        processor.clean_data()
        processor.calculate_totals()
        processor.save_clean_data(clean_file)
        
        df_clean = processor.get_clean_data()
        print(f"Datos procesados: {len(df_clean)} filas válidas")
        
        # 2. Análisis de datos
        print("\n2. Realizando análisis...")
        analyzer = SalesAnalyzer(df_clean)
        results = analyzer.get_resumen_completo()
        
        # Mostrar resultados
        print(f"\nProducto más vendido: {results['producto_mas_vendido']['producto']} "
              f"({results['producto_mas_vendido']['cantidad_total']} unidades)")
        
        print(f"Producto mayor facturación: {results['producto_mayor_facturacion']['producto']} "
              f"(${results['producto_mayor_facturacion']['facturacion_total']:,.2f})")
        
        print("\nFacturación mensual:")
        for mes, facturacion in results['facturacion_mensual'].items():
            print(f"  {mes}: ${facturacion:,.2f}")
        
        # 3. Guardar en base de datos
        print("\n3. Guardando en base de datos...")
        db = DatabaseManager()
        db.insert_ventas_data(df_clean)
        db.save_analysis_results(results)
        
        # Verificar con consulta SQL
        print("\n4. Verificando con consulta SQL - Top 3 productos:")
        top_productos = db.get_top_productos_query(3)
        for _, row in top_productos.iterrows():
            print(f"  {row['producto']}: {row['cantidad_total']} unidades")
        
        print(f"\nProceso completado exitosamente!")
        print(f"- Datos limpios guardados en: {clean_file}")
        print(f"- Base de datos SQLite en: {db.db_path}")
        print("- Ejecuta 'python -m src.visualizer' para generar gráficos")
        print("- Ejecuta 'pytest' para correr las pruebas")
        
    except Exception as e:
        print(f"Error durante el procesamiento: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()