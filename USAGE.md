# 🚀 Guía de Uso - Análisis de Ventas

Este proyecto ofrece **dos formas** de ejecutar el análisis de ventas:

---

## 📊 Opción 1: Interfaz Gráfica (GUI) - **Recomendado para usuarios**

### ¿Cuándo usar?
- Eres un usuario de ventas/negocio (no técnico)
- Prefieres una interfaz visual intuitiva
- Quieres ver resultados de forma rápida y visual

### ¿Cómo ejecutar?

```powershell
# Ejecutar la aplicación con interfaz gráfica
python app.py
```

### Flujo de trabajo:
1. **Abre la aplicación** → Ventana con área de carga
2. **Selecciona tu archivo** → Click en "Seleccionar Archivo" o arrastra el CSV
3. **Preview de datos** → Verifica las primeras filas
4. **Opciones** → Marca "✓ Generar gráficos" (activado por defecto)
5. **Analizar** → Click en el botón verde "Analizar"
6. **Resultados** → Ve métricas, top 3 productos y botones para:
   - 📊 Abrir Excel (se abre automáticamente)
   - 📈 Ver Gráficos (abre la carpeta)
   - 🔄 Nuevo Análisis

### Características:
- ✅ Drag & Drop para cargar archivos
- ✅ Vista previa de datos
- ✅ Barra de progreso en tiempo real
- ✅ Resumen ejecutivo con métricas clave
- ✅ Top 3 productos más vendidos
- ✅ Acceso directo a resultados

---

## 💻 Opción 2: Línea de Comandos (CLI) - **Para desarrolladores**

### ¿Cuándo usar?
- Eres desarrollador o usuario técnico
- Quieres automatizar el proceso
- Necesitas integrar con otros scripts
- Prefieres control total desde terminal

### ¿Cómo ejecutar?

```powershell
# Ejecutar análisis completo desde terminal
python main.py
```

### Requisitos previos:
1. Coloca tu archivo CSV en: `data/raw/ventas.csv`
2. El CSV debe tener las columnas: `fecha`, `producto`, `cantidad`, `precio_unitario`

### Flujo de trabajo:
```
=== ANÁLISIS DE VENTAS ===

1. Cargando y limpiando datos...
Filas eliminadas en limpieza: X
Datos procesados: Y filas válidas

2. Realizando análisis...
Producto más vendido: [Producto X] (Z unidades)
Producto mayor facturación: [Producto Y] ($XX,XXX.XX)

Facturación mensual:
  2024-01: $XX,XXX.XX
  2024-02: $XX,XXX.XX
  ...

3. Guardando en base de datos...
Insertadas Y filas en tabla ventas
Resultados de análisis guardados en BD

4. Verificando con consulta SQL - Top 3 productos:
  [Producto 1]: XXX unidades
  [Producto 2]: XXX unidades
  [Producto 3]: XXX unidades

Proceso completado exitosamente!
- Datos limpios guardados en: data/processed/ventas_clean.csv
- Base de datos SQLite en: output/database/ventas.db
```

### Comandos adicionales:

```powershell
# Generar solo gráficos (después de ejecutar main.py)
python -m src.visualizer

# Ejecutar tests
pytest

# Ejecutar tests con cobertura
pytest --cov=src tests/
```

---

## 📁 Outputs generados (ambas opciones)

### Archivos creados:
```
output/
├── analisis_ventas.xlsx       # Excel con datos y estadísticas
├── database/
│   └── ventas.db              # Base de datos SQLite
└── graficos/                  # Gráficos generados
    ├── ventas_por_producto.png
    ├── facturacion_mensual.png
    └── ...

data/processed/
└── ventas_clean.csv           # Datos limpios (solo CLI)
```

---

## 🔄 Comparación rápida

| Característica | GUI (`app.py`) | CLI (`main.py`) |
|----------------|----------------|-----------------|
| **Facilidad de uso** | ⭐⭐⭐⭐⭐ Muy fácil | ⭐⭐⭐ Requiere terminal |
| **Velocidad** | ⭐⭐⭐⭐ Rápido | ⭐⭐⭐⭐⭐ Más rápido |
| **Visualización** | ⭐⭐⭐⭐⭐ Resumen visual | ⭐⭐⭐ Solo texto |
| **Automatización** | ⭐⭐ Manual | ⭐⭐⭐⭐⭐ Scriptable |
| **Flexibilidad** | ⭐⭐⭐ Opciones básicas | ⭐⭐⭐⭐⭐ Control total |
| **Usuario objetivo** | Negocio/Ventas | Desarrolladores/Data |

---

## 🆘 Solución de problemas comunes

### Error: "Archivo no encontrado"
- **GUI:** Asegúrate de seleccionar un archivo CSV o Excel válido
- **CLI:** Coloca tu archivo en `data/raw/ventas.csv`

### Error: "No module named 'X'"
```powershell
# Instalar todas las dependencias
pip install -r requirements.txt
```

### Error: "DatabaseManager object has no attribute..."
- Ya está corregido en la versión actual
- El método correcto es `insert_ventas_data()`, no `save_sales_data()`

### CSV con formato incorrecto
Tu archivo debe tener estas columnas:
- `fecha` (formato: YYYY-MM-DD o similar)
- `producto` (texto)
- `cantidad` (número entero)
- `precio_unitario` (número decimal)

---

## 📧 Contacto y Soporte

Si tienes dudas o problemas:
1. Revisa esta guía primero
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que tu CSV tenga el formato correcto
4. Abre un issue en GitHub con el error completo

---

**¡Feliz análisis! 📊**
