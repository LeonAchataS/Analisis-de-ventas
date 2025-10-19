import pandas as pd

class SalesAnalyzer:
    
    def __init__(self, df):
        self.df = df
    
    def producto_mas_vendido(self):
        """Calcula el producto más vendido por cantidad"""
        ventas_por_producto = self.df.groupby('producto')['cantidad'].sum()
        producto_top = ventas_por_producto.idxmax()
        cantidad_top = ventas_por_producto.max()
        
        return {
            'producto': producto_top,
            'cantidad_total': cantidad_top
        }
    
    def producto_mayor_facturacion(self):
        """Calcula el producto con mayor facturación total"""
        facturacion_por_producto = self.df.groupby('producto')['total'].sum()
        producto_top = facturacion_por_producto.idxmax()
        facturacion_top = facturacion_por_producto.max()
        
        return {
            'producto': producto_top,
            'facturacion_total': facturacion_top
        }
    
    def facturacion_por_mes(self):
        """Calcula la facturación total por mes"""
        # Trabajar con copia para no modificar el DataFrame original
        df_temp = self.df.copy()
        df_temp['año_mes'] = df_temp['fecha'].dt.to_period('M')
        facturacion_mensual = df_temp.groupby('año_mes')['total'].sum()
        
        return facturacion_mensual.to_dict()
    
    def get_top_productos_cantidad(self, top_n=3):
        """Obtiene los top N productos por cantidad"""
        ventas_por_producto = self.df.groupby('producto')['cantidad'].sum()
        return ventas_por_producto.nlargest(top_n).to_dict()
    
    def get_top_productos_facturacion(self, top_n=3):
        """Obtiene los top N productos por facturación"""
        facturacion_por_producto = self.df.groupby('producto')['total'].sum()
        return facturacion_por_producto.nlargest(top_n).to_dict()
    
    def get_resumen_completo(self):
        """Genera resumen completo de análisis"""
        return {
            'producto_mas_vendido': self.producto_mas_vendido(),
            'producto_mayor_facturacion': self.producto_mayor_facturacion(),
            'facturacion_mensual': self.facturacion_por_mes(),
            'top_3_cantidad': self.get_top_productos_cantidad(),
            'top_3_facturacion': self.get_top_productos_facturacion()
        }