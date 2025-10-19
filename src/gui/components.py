"""
Componentes reutilizables para la GUI.
"""

import tkinter as tk
from tkinter import ttk
from src.gui.styles import *


class DropZone(tk.Frame):
    """Widget para área de drag and drop."""
    
    def __init__(self, parent, on_drop_callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_drop_callback = on_drop_callback
        
        self.config(
            bg=LIGHT_GRAY,
            highlightbackground=PRIMARY_COLOR,
            highlightthickness=2,
            relief=tk.FLAT,
            bd=0
        )
        
        # Icono y texto
        self.icon_label = tk.Label(
            self,
            text="📁",
            font=(FONT_FAMILY, 48),
            bg=LIGHT_GRAY,
            fg=PRIMARY_COLOR
        )
        self.icon_label.pack(pady=(40, 10))
        
        self.text_label = tk.Label(
            self,
            text="Arrastra tu archivo CSV aquí\no haz clic para seleccionar",
            font=(FONT_FAMILY, FONT_SIZE_SUBTITLE),
            bg=LIGHT_GRAY,
            fg=DARK_GRAY,
            justify=tk.CENTER
        )
        self.text_label.pack(pady=(0, 40))
        
        # Click para abrir file dialog
        self.bind('<Button-1>', lambda e: on_drop_callback(None))
        self.icon_label.bind('<Button-1>', lambda e: on_drop_callback(None))
        self.text_label.bind('<Button-1>', lambda e: on_drop_callback(None))
        
        # Efectos hover
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        """Efecto hover."""
        self.config(bg="#D6E4F0")
        self.icon_label.config(bg="#D6E4F0")
        self.text_label.config(bg="#D6E4F0")
    
    def _on_leave(self, event):
        """Quita efecto hover."""
        self.config(bg=LIGHT_GRAY)
        self.icon_label.config(bg=LIGHT_GRAY)
        self.text_label.config(bg=LIGHT_GRAY)


class MetricCard(tk.Frame):
    """Card para mostrar una métrica."""
    
    def __init__(self, parent, title, value, icon="", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.config(
            bg="white",
            highlightbackground=LIGHT_GRAY,
            highlightthickness=1,
            relief=tk.FLAT,
            bd=0
        )
        
        # Contenedor
        container = tk.Frame(self, bg="white")
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Icono
        if icon:
            icon_label = tk.Label(
                container,
                text=icon,
                font=(FONT_FAMILY, 24),
                bg="white"
            )
            icon_label.pack(anchor=tk.W)
        
        # Título
        title_label = tk.Label(
            container,
            text=title,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            fg=DARK_GRAY,
            bg="white"
        )
        title_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Valor
        self.value_label = tk.Label(
            container,
            text=value,
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
            fg=PRIMARY_COLOR,
            bg="white"
        )
        self.value_label.pack(anchor=tk.W, pady=(5, 0))
    
    def update_value(self, new_value):
        """Actualiza el valor de la métrica."""
        self.value_label.config(text=new_value)


class ProgressFrame(tk.Frame):
    """Frame para mostrar progreso del procesamiento."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg=BG_COLOR)
        
        # Título
        self.title_label = tk.Label(
            self,
            text="Procesando análisis...",
            font=(FONT_FAMILY, FONT_SIZE_SUBTITLE, "bold"),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        )
        self.title_label.pack(pady=(20, 10))
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            self,
            mode='indeterminate',
            length=400
        )
        self.progress_bar.pack(pady=10)
        
        # Mensaje de estado
        self.status_label = tk.Label(
            self,
            text="Iniciando...",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL),
            fg=DARK_GRAY,
            bg=BG_COLOR
        )
        self.status_label.pack(pady=5)
        
        # Log de pasos
        self.log_frame = tk.Frame(self, bg=BG_COLOR)
        self.log_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.log_labels = []
    
    def start(self):
        """Inicia la barra de progreso."""
        self.progress_bar.start(10)
    
    def stop(self):
        """Detiene la barra de progreso."""
        self.progress_bar.stop()
    
    def update_status(self, message):
        """Actualiza el mensaje de estado."""
        self.status_label.config(text=message)
    
    def add_log(self, message, success=True):
        """Añade un mensaje al log."""
        icon = "✓" if success else "⚠"
        color = SUCCESS_COLOR if success else WARNING_COLOR
        
        log_label = tk.Label(
            self.log_frame,
            text=f"{icon} {message}",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            fg=color,
            bg=BG_COLOR,
            anchor=tk.W
        )
        log_label.pack(anchor=tk.W, pady=2)
        self.log_labels.append(log_label)
        
        # Auto-scroll
        self.update_idletasks()


class DataPreviewTable(ttk.Treeview):
    """Tabla para preview de datos."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Scrollbars
        vsb = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_dataframe(self, df, max_rows=5):
        """Carga un DataFrame en la tabla."""
        # Limpiar tabla
        self.delete(*self.get_children())
        
        # Configurar columnas
        self['columns'] = list(df.columns)
        self['show'] = 'headings'
        
        # Headers
        for col in df.columns:
            self.heading(col, text=col)
            self.column(col, width=120, anchor=tk.W)
        
        # Datos (primeras filas)
        for idx, row in df.head(max_rows).iterrows():
            values = [str(val) for val in row]
            self.insert('', tk.END, values=values)
