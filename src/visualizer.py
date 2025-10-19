import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from .database import DatabaseManager

class SalesVisualizer:
    
    def __init__(self):
        self.output_dir = "output/graficos"
        self.ensure_directory()
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def ensure_directory(self):
        """Crea directorio de salida si no existe"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generar_grafico_mensual(self, save_path="grafico.png"):
        """Genera gráfico de facturación total por mes"""
        
        # Obtener datos desde BD
        db = DatabaseManager()
        df_mensual = db.get_facturacion_mensual_query()
        
        if df_mensual.empty:
            print("No hay datos para generar gráfico")
            return
        
        # Crear gráfico
        plt.figure(figsize=(12, 6))
        
        # Convertir mes a datetime para mejor visualización
        df_mensual['mes_dt'] = pd.to_datetime(df_mensual['mes'])
        
        # Gráfico de barras
        bars = plt.bar(df_mensual['mes'], df_mensual['facturacion_total'], 
                      color='steelblue', alpha=0.7, edgecolor='navy')
        
        # Personalización
        plt.title('Facturación Total por Mes', fontsize=16, fontweight='bold')
        plt.xlabel('Mes', fontsize=12)
        plt.ylabel('Facturación Total ($)', fontsize=12)
        plt.xticks(rotation=45)
        
        # Agregar valores en las barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}',
                    ha='center', va='bottom', fontsize=10)
        
        # Formatear eje Y
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Ajustar layout
        plt.tight_layout()
        plt.grid(axis='y', alpha=0.3)
        
        # Guardar
        full_path = os.path.join(self.output_dir, save_path)
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Gráfico guardado en: {full_path}")
        return full_path
    
    def generar_grafico_productos(self, top_n=5):
        """Genera gráfico de top productos por cantidad"""
        
        db = DatabaseManager()
        df_productos = db.get_top_productos_query(top_n)
        
        plt.figure(figsize=(10, 6))
        
        # Gráfico horizontal
        bars = plt.barh(df_productos['producto'], df_productos['cantidad_total'],
                       color='lightcoral', alpha=0.7, edgecolor='darkred')
        
        plt.title(f'Top {top_n} Productos por Cantidad Vendida', fontsize=16, fontweight='bold')
        plt.xlabel('Cantidad Total', fontsize=12)
        plt.ylabel('Producto', fontsize=12)
        
        # Agregar valores
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{width:,.0f}',
                    ha='left', va='center', fontsize=10)
        
        plt.tight_layout()
        
        save_path = os.path.join(self.output_dir, 'top_productos.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Gráfico de productos guardado en: {save_path}")
        return save_path

def main():
    """Función principal para generar gráficos"""
    print("Generando visualizaciones...")
    
    visualizer = SalesVisualizer()
    
    try:
        # Generar gráfico principal
        visualizer.generar_grafico_mensual()
        
        # Generar gráfico adicional
        visualizer.generar_grafico_productos()
        
        print("Visualizaciones completadas exitosamente!")
        
    except Exception as e:
        print(f"Error al generar gráficos: {str(e)}")

if __name__ == "__main__":
    main()