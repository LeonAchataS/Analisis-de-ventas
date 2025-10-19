"""
Ventana principal de la aplicación.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
import pandas as pd
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.gui.styles import *
from src.gui.components import DropZone, MetricCard, ProgressFrame, DataPreviewTable
from src.data_processor import DataProcessor
from src.analyzer import SalesAnalyzer
from src.visualizer import SalesVisualizer
from src.database import DatabaseManager


class MainWindow:
    """Ventana principal de la aplicación de análisis de ventas."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis Automático de Ventas")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        
        # Variables
        self.current_file = None
        self.df = None
        self.processed_df = None
        self.results = {}
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear frames principales
        self.create_widgets()
        
        # Centrar ventana
        self.center_window()
    
    def setup_styles(self):
        """Configura los estilos de ttk."""
        style = ttk.Style()
        
        # Intentar usar un tema moderno
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'vista' in available_themes:
            style.theme_use('vista')
        
        # Configurar estilos personalizados
        for widget_name, config in TTK_STYLE_CONFIG.items():
            if 'configure' in config:
                style.configure(widget_name, **config['configure'])
    
    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Crea los widgets de la ventana."""
        # Frame principal con scroll
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y Scrollbar para hacer toda la ventana scrolleable
        self.canvas = tk.Canvas(main_frame, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_window = self.canvas.create_window((PADDING, PADDING), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Ajustar el ancho del frame al canvas
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel para scroll
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Header
        self.create_header(self.scrollable_frame)
    
    def _on_canvas_configure(self, event):
        """Ajusta el ancho del frame interior al canvas."""
        canvas_width = event.width - PADDING * 2
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        # Container para diferentes vistas
        self.content_frame = tk.Frame(self.scrollable_frame, bg=BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Vista inicial (drop zone)
        self.show_upload_view()
    
    def create_header(self, parent):
        """Crea el header de la aplicación."""
        header_frame = tk.Frame(parent, bg=BG_COLOR)
        header_frame.pack(fill=tk.X)
        
        # Título
        title = ttk.Label(
            header_frame,
            text="📊 Análisis Automático de Ventas",
            style="Title.TLabel"
        )
        title.pack(anchor=tk.W)
        
        # Subtítulo
        subtitle = ttk.Label(
            header_frame,
            text="Procesa tus datos de ventas y obtén insights automáticamente",
            style="Subtitle.TLabel"
        )
        subtitle.pack(anchor=tk.W, pady=(5, 0))
        
        # Separador
        separator = ttk.Separator(header_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=(15, 0))
    
    def show_upload_view(self):
        """Muestra la vista de carga de archivo."""
        self.clear_content()
        
        # Drop zone
        drop_zone = DropZone(
            self.content_frame,
            on_drop_callback=self.handle_file_selection
        )
        drop_zone.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Botón de selección alternativo
        btn_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        btn_frame.pack(pady=10)
        
        select_btn = tk.Button(
            btn_frame,
            text="Seleccionar Archivo",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=SECONDARY_COLOR,
            activeforeground="white",
            cursor="hand2",
            padx=30,
            pady=12,
            relief=tk.FLAT,
            command=lambda: self.handle_file_selection(None)
        )
        select_btn.pack()
    
    def show_preview_view(self):
        """Muestra la vista de preview y opciones."""
        self.clear_content()
        
        # Título
        title = ttk.Label(
            self.content_frame,
            text=f"Archivo: {os.path.basename(self.current_file)}",
            style="Subtitle.TLabel"
        )
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Info del archivo
        info_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_text = f"📄 {len(self.df)} filas  |  📋 {len(self.df.columns)} columnas"
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=(FONT_FAMILY, FONT_SIZE_NORMAL),
            fg=DARK_GRAY,
            bg=BG_COLOR
        )
        info_label.pack(anchor=tk.W)
        
        # Preview de datos
        preview_label = tk.Label(
            self.content_frame,
            text="Vista previa de los datos:",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        )
        preview_label.pack(anchor=tk.W, pady=(10, 5))
        
        preview_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        preview_table = DataPreviewTable(preview_frame)
        preview_table.pack(fill=tk.BOTH, expand=True)
        preview_table.load_dataframe(self.df, max_rows=5)
        
        # Opciones
        options_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        options_frame.pack(fill=tk.X, pady=(10, 0))
        
        options_label = tk.Label(
            options_frame,
            text="Opciones de análisis:",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        )
        options_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.option_graficos = tk.BooleanVar(value=True)
        
        check_graficos = tk.Checkbutton(
            options_frame,
            text="✓ Generar gráficos",
            variable=self.option_graficos,
            font=(FONT_FAMILY, FONT_SIZE_NORMAL),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            selectcolor=BG_COLOR,
            activebackground=BG_COLOR
        )
        check_graficos.pack(anchor=tk.W, pady=2)
        
        # Botones de acción
        btn_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancelar",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL),
            bg=LIGHT_GRAY,
            fg=TEXT_COLOR,
            activebackground=DARK_GRAY,
            activeforeground="white",
            cursor="hand2",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            command=self.show_upload_view
        )
        cancel_btn.pack(side=tk.LEFT)
        
        analyze_btn = tk.Button(
            btn_frame,
            text="Analizar",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=SECONDARY_COLOR,
            activeforeground="white",
            cursor="hand2",
            padx=40,
            pady=10,
            relief=tk.FLAT,
            command=self.start_analysis
        )
        analyze_btn.pack(side=tk.RIGHT)
    
    def show_progress_view(self):
        """Muestra la vista de progreso."""
        self.clear_content()
        
        self.progress_frame = ProgressFrame(self.content_frame)
        self.progress_frame.pack(fill=tk.BOTH, expand=True)
        self.progress_frame.start()
    
    def show_results_view(self):
        """Muestra la vista de resultados."""
        self.clear_content()
        
        # Título de éxito
        success_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        success_frame.pack(fill=tk.X, pady=(0, 20))
        
        success_icon = tk.Label(
            success_frame,
            text="✓",
            font=(FONT_FAMILY, 48),
            fg=SUCCESS_COLOR,
            bg=BG_COLOR
        )
        success_icon.pack()
        
        success_label = tk.Label(
            success_frame,
            text="¡Análisis completado con éxito!",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
            fg=SUCCESS_COLOR,
            bg=BG_COLOR
        )
        success_label.pack(pady=(10, 0))
        
        # Resumen ejecutivo
        summary_label = tk.Label(
            self.content_frame,
            text="📊 Resumen Ejecutivo",
            font=(FONT_FAMILY, FONT_SIZE_SUBTITLE, "bold"),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        )
        summary_label.pack(anchor=tk.W, pady=(10, 10))
        
        # Grid de métricas (solo 3 métricas ahora)
        metrics_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        metrics_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Configurar grid para 3 columnas
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_columnconfigure(2, weight=1)
        
        # Métrica: Total de ventas
        total_ventas = self.results.get('total_ventas', 0)
        total_ventas_formatted = f"${total_ventas:,.2f}"
        
        card_ventas = MetricCard(
            metrics_frame,
            title="Total de Ventas",
            value=total_ventas_formatted,
            icon="💰"
        )
        card_ventas.grid(row=0, column=0, sticky="ew", padx=(0, 7), pady=5)
        
        # Métrica: Número de transacciones
        num_transacciones = self.results.get('num_transacciones', 0)
        
        card_transacciones = MetricCard(
            metrics_frame,
            title="Transacciones",
            value=f"{num_transacciones:,}",
            icon="📝"
        )
        card_transacciones.grid(row=0, column=1, sticky="ew", padx=(7, 7), pady=5)
        
        # Métrica: Venta promedio
        ticket_promedio = self.results.get('ticket_promedio', 0)
        ticket_promedio_formatted = f"${ticket_promedio:,.2f}"
        
        card_ticket = MetricCard(
            metrics_frame,
            title="Venta Promedio",
            value=ticket_promedio_formatted,
            icon="🎫"
        )
        card_ticket.grid(row=0, column=2, sticky="ew", padx=(7, 0), pady=5)
        
        # Top 3 productos
        top_productos = self.results.get('top_productos', [])
        
        if top_productos and len(top_productos) > 0:
            top_label = tk.Label(
                self.content_frame,
                text="🏆 Top 3 Productos Más Vendidos",
                font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
                fg=TEXT_COLOR,
                bg=BG_COLOR
            )
            top_label.pack(anchor=tk.W, pady=(15, 10))
            
            top_frame = tk.Frame(self.content_frame, bg="white", highlightbackground=LIGHT_GRAY, highlightthickness=1)
            top_frame.pack(fill=tk.X, pady=(0, 20))
            
            for idx, (producto, ventas) in enumerate(top_productos[:3], 1):
                producto_frame = tk.Frame(top_frame, bg="white")
                producto_frame.pack(fill=tk.X, padx=15, pady=8)
                
                # Número
                num_label = tk.Label(
                    producto_frame,
                    text=f"#{idx}",
                    font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
                    fg=PRIMARY_COLOR,
                    bg="white",
                    width=3
                )
                num_label.pack(side=tk.LEFT)
                
                # Nombre del producto
                nombre_label = tk.Label(
                    producto_frame,
                    text=producto,
                    font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                    fg=TEXT_COLOR,
                    bg="white",
                    anchor=tk.W
                )
                nombre_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
                
                # Ventas
                ventas_label = tk.Label(
                    producto_frame,
                    text=f"${ventas:,.2f}",
                    font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
                    fg=SUCCESS_COLOR,
                    bg="white"
                )
                ventas_label.pack(side=tk.RIGHT)
        
        # Botones de acción
        btn_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botón: Abrir Excel
        excel_btn = tk.Button(
            btn_frame,
            text="📊 Abrir Excel",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            bg=SUCCESS_COLOR,
            fg="white",
            activebackground="#058a69",
            activeforeground="white",
            cursor="hand2",
            padx=20,
            pady=12,
            relief=tk.FLAT,
            command=self.open_excel
        )
        excel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón: Ver Gráficos (si se generaron)
        if self.option_graficos.get():
            graficos_btn = tk.Button(
                btn_frame,
                text="📈 Ver Gráficos",
                font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
                bg=PRIMARY_COLOR,
                fg="white",
                activebackground=SECONDARY_COLOR,
                activeforeground="white",
                cursor="hand2",
                padx=20,
                pady=12,
                relief=tk.FLAT,
                command=self.open_graficos
            )
            graficos_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón: Nuevo Análisis
        new_btn = tk.Button(
            btn_frame,
            text="🔄 Nuevo Análisis",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL),
            bg=LIGHT_GRAY,
            fg=TEXT_COLOR,
            activebackground=DARK_GRAY,
            activeforeground="white",
            cursor="hand2",
            padx=20,
            pady=12,
            relief=tk.FLAT,
            command=self.show_upload_view
        )
        new_btn.pack(side=tk.RIGHT)
    
    def clear_content(self):
        """Limpia el frame de contenido."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def handle_file_selection(self, filepath):
        """Maneja la selección de archivo."""
        if filepath is None:
            # Abrir file dialog
            filepath = filedialog.askopenfilename(
                title="Seleccionar archivo de ventas",
                filetypes=[
                    ("CSV files", "*.csv"),
                    ("Excel files", "*.xlsx"),
                    ("All files", "*.*")
                ]
            )
        
        if not filepath:
            return
        
        # Validar extensión
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in ['.csv', '.xlsx']:
            messagebox.showerror(
                "Error",
                "Por favor selecciona un archivo CSV o Excel válido."
            )
            return
        
        try:
            # Cargar datos
            if ext == '.csv':
                self.df = pd.read_csv(filepath)
            else:
                self.df = pd.read_excel(filepath)
            
            self.current_file = filepath
            self.show_preview_view()
            
        except Exception as e:
            messagebox.showerror(
                "Error al cargar archivo",
                f"No se pudo cargar el archivo:\n{str(e)}"
            )
    
    def start_analysis(self):
        """Inicia el análisis en un thread separado."""
        self.show_progress_view()
        
        # Ejecutar análisis en thread
        thread = threading.Thread(target=self.run_analysis)
        thread.daemon = True
        thread.start()
    
    def run_analysis(self):
        """Ejecuta el análisis de datos."""
        try:
            # 1. Limpieza de datos
            self.update_progress("Limpiando datos...")
            processor = DataProcessor()
            processor.df = self.df.copy()
            self.processed_df = processor.clean_data()
            processor.calculate_totals()
            self.processed_df = processor.df
            self.log_step("Datos limpiados correctamente", success=True)
            
            # 2. Análisis
            self.update_progress("Calculando estadísticas...")
            analyzer = SalesAnalyzer(self.processed_df)
            
            # Obtener estadísticas
            top_facturacion = analyzer.get_top_productos_facturacion(top_n=3)
            
            # Convertir dict a lista de tuplas para mostrar
            top_productos_list = [(producto, ventas) for producto, ventas in top_facturacion.items()]
            
            stats = {
                'total_ventas': self.processed_df['total'].sum() if 'total' in self.processed_df.columns else 0,
                'ticket_promedio': self.processed_df['total'].mean() if 'total' in self.processed_df.columns else 0,
                'top_productos': top_productos_list,
            }
            
            self.log_step("Estadísticas calculadas", success=True)
            
            # 3. Guardar en base de datos
            self.update_progress("Guardando en base de datos...")
            db_manager = DatabaseManager()
            db_manager.insert_ventas_data(self.processed_df)
            self.log_step("Datos guardados en BD", success=True)
            
            # 4. Generar gráficos (si está activado)
            graficos_paths = []
            if self.option_graficos.get():
                self.update_progress("Generando gráficos...")
                visualizer = SalesVisualizer()
                # Generar gráficos desde la BD
                path1 = visualizer.generar_grafico_mensual('facturacion_mensual.png')
                path2 = visualizer.generar_grafico_productos(top_n=5)
                graficos_paths = [path1, path2]
                self.log_step(f"{len(graficos_paths)} gráficos generados", success=True)
            
            # 5. Exportar a Excel
            self.update_progress("Generando archivo Excel...")
            output_path = self.export_to_excel(stats)
            self.log_step("Excel generado correctamente", success=True)
            
            # 6. Preparar resultados
            self.results = {
                'total_ventas': stats.get('total_ventas', 0),
                'num_transacciones': len(self.processed_df),
                'ticket_promedio': stats.get('ticket_promedio', 0),
                'top_productos': stats.get('top_productos', []),
                'output_path': output_path,
                'graficos_paths': graficos_paths
            }
            
            # 7. Mostrar resultados
            self.update_progress("¡Completado!")
            self.root.after(500, self.show_results_view)
            
        except Exception as e:
            error_msg = str(e)
            self.log_step(f"Error: {error_msg}", success=False)
            self.root.after(100, lambda msg=error_msg: messagebox.showerror(
                "Error en el análisis",
                f"Ocurrió un error durante el análisis:\n{msg}"
            ))
            self.root.after(200, self.show_upload_view)
    
    def update_progress(self, message):
        """Actualiza el mensaje de progreso."""
        if hasattr(self, 'progress_frame'):
            self.root.after(0, lambda: self.progress_frame.update_status(message))
    
    def log_step(self, message, success=True):
        """Añade un mensaje al log."""
        if hasattr(self, 'progress_frame'):
            self.root.after(0, lambda: self.progress_frame.add_log(message, success))
    
    def export_to_excel(self, stats):
        """Exporta los resultados a Excel."""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        output_path = output_dir / "analisis_ventas.xlsx"
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Hoja 1: Datos procesados
            self.processed_df.to_excel(writer, sheet_name='Datos', index=False)
            
            # Hoja 2: Estadísticas
            stats_df = pd.DataFrame([stats])
            stats_df.to_excel(writer, sheet_name='Estadísticas', index=False)
            
            # Hoja 3: Top productos
            if 'top_productos' in stats:
                top_df = pd.DataFrame(
                    stats['top_productos'],
                    columns=['Producto', 'Ventas']
                )
                top_df.to_excel(writer, sheet_name='Top Productos', index=False)
        
        return str(output_path)
    
    def open_excel(self):
        """Abre el archivo Excel generado."""
        if 'output_path' in self.results:
            try:
                os.startfile(self.results['output_path'])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{str(e)}")
    
    def open_graficos(self):
        """Abre la carpeta de gráficos."""
        graficos_dir = Path("output/graficos")
        if graficos_dir.exists():
            try:
                os.startfile(str(graficos_dir))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la carpeta:\n{str(e)}")


def main():
    """Función principal."""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
