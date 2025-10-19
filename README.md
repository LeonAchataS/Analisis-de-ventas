# 📊 Sistema de Análisis de Ventas# Análisis de Ventas

Sistema profesional de análisis de datos de ventas diseñado con **arquitectura modular**. Procesa archivos CSV, realiza análisis estadísticos avanzados, persiste resultados en SQLite y genera visualizaciones profesionales de alta calidad.Sistema de análisis de datos de ventas que procesa archivos CSV, realiza análisis estadísticos, persiste resultados en SQLite y genera visualizaciones.

--- 

## Estructura del Proyecto

proyecto_ventas/
├── data/
│   ├── raw/
│   │   └── ventas.csv
│   └── processed/
│       └── ventas_clean.csv
├── src/
│   ├── __init__.py
│   ├── data_processor.py      # Carga y limpieza de datos
│   ├── analyzer.py            # Análisis de ventas
│   ├── database.py            # Operaciones de BD
│   └── visualizer.py          # Generación de gráficos
├── tests/
│   ├── __init__.py
│   ├── test_data_processor.py
│   ├── test_analyzer.py
│   └── conftest.py            # Configuración de pytest
├── output/
│   ├── graficos/
│   │   └── grafico.png
│   └── database/
│       └── ventas.db
├── sql/
│   └── queries.sql            # Consultas SQL predefinidas
├── requirements.txt
├── main.py                    # Script principal
└── README.md

### 1. **Modularidad y Mantenibilidad**

Cada componente puede modificarse independientemente sin romper el resto del sistema.

- Cambiar la lógica de limpieza no afecta al análisis
- Agregar nuevos análisis no requiere tocar la BDfrom src.data_processor import DataProcessor
- Cambiar el formato de gráficos no afecta al procesamientofrom src.analyzer import SalesAnalyzer


### 2. **Escalabilidad** 

El diseño permite escalar fácilmente: processor.load_data("data/raw/ventas.csv")

- Procesar archivos de millones de registros (pandas optimizado) processor.clean_data()
- Agregar nuevos tipos de análisis sin duplicar códigoprocessor.calculate_totals()
- Migrar a bases de datos más robustas (PostgreSQL, MongoDB)
- Paralelizar procesamiento de múltiples archivosanalyzer = SalesAnalyzer(processor.get_clean_data())

### 3. **Testabilidad**

Cada módulo puede testearse aisladamente:

- Tests unitarios para cada función
- Mocks simples para dependencias
- Tests de integración end-to-end- `data/processed/ventas_clean.csv`: Datos limpios
- `output/database/ventas.db`: Base de datos SQLite

### 4. **Reutilización**

- Los módulos son reutilizables en otros proyectos:- `output/graficos/top_productos.png`: Gráfico de top productos


### 5. **Manejo de Errores Robusto** 

- Validaciones en cada etapa del pipeline- Verificar que el CSV tenga datos válidos
- Mensajes de error descriptivos- Revisar que fechas estén en formato correcto
- Try-catch con contexto específico- Confirmar que cantidades y precios sean positivos
- Creación automática de directorios

### 6. **Documentación y Legibilidad** 

- Docstrings en todas las funciones - Asegurar que no haya otro proceso usando la BD
- Nombres descriptivos de variables
- Comentarios explicativos en lógica compleja
- README completo (este documento)

## 💻 Requisitos del Sistema

### Requisitos Mínimos

- **Python:** 3.8 o superior

- **Sistema Operativo:** Windows, Linux, macOSPara agregar nuevos tests, crear archivos en `tests/` siguiendo el patrón `test_*.py`.
- **RAM:** 512 MB (para datasets pequeños/medianos)
- **Espacio en disco:** 50 MB

### Dependencias Principales
```
pandas==2.3.3 # Procesamiento de datos
matplotlib==3.10.7 # Visualizaciones base
seaborn==0.13.2 # Estilos de gráficos
pytest==8.4.2 # Testing automatizado
```

---

## 📥 Instalación Paso a Paso

### 1. Clonar o Descargar el Proyecto
```bash
# Si tienes git:
git clone <url-del-repositorio>
cd proyecto_ventas

# O simplemente descarga el ZIP y descomprímelo
```

### 2. Crear Entorno Virtual (Recomendado)

**En Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

**Verificar instalación:**
```bash
pip list
```

Deberías ver: pandas, matplotlib, seaborn, pytest.

---

## 📊 Preparación de Datos

### Formato del Archivo CSV

El archivo `ventas.csv` debe estar en `data/raw/` con las siguientes columnas:

| Columna           | Tipo    | Descripción                          | Ejemplo      |
|-------------------|---------|--------------------------------------|--------------|
| `fecha`           | string  | Fecha en formato YYYY-MM-DD         | 2023-01-15   |
| `producto`        | string  | Nombre del producto                 | Laptop HP    |
| `cantidad`        | integer | Cantidad vendida (positivo)         | 5            |
| `precio_unitario` | float   | Precio por unidad (positivo)        | 1250.50      |

### Ejemplo de CSV válido:
```csv
fecha,producto,cantidad,precio_unitario
2023-01-15,Laptop HP,2,1200.00
2023-01-16,Mouse Logitech,5,25.50
2023-01-17,Teclado Mecánico,3,89.99
2023-02-01,Monitor Dell,1,450.00
2023-02-05,Laptop HP,4,1200.00
```

### Validaciones Automáticas

El sistema **automáticamente elimina**:

- ❌ Filas con valores nulos en cualquier columna
- ❌ Fechas inválidas o no parseables
- ❌ Cantidades negativas o cero
- ❌ Precios negativos o cero
- ❌ Productos con nombre vacío

**Nota:** El sistema reporta cuántas filas fueron eliminadas durante la limpieza.

---

## 🎬 Ejecución del Sistema

### Opción 1: Pipeline Completo (Recomendado)

Ejecuta todo el proceso de análisis con un solo comando:

```bash
python main.py
```

**¿Qué hace este comando?**

1. **Carga de Datos** 📥
   - Lee `data/raw/ventas.csv`
   - Muestra cantidad de filas leídas

2. **Limpieza de Datos** 🧹
   - Aplica todas las validaciones
   - Convierte fechas a formato datetime
   - Filtra datos inconsistentes
   - Reporta filas eliminadas

3. **Cálculo de Totales** 🔢
   - Genera columna `total = cantidad × precio_unitario`
   - Guarda datos limpios en `data/processed/ventas_clean.csv`

4. **Análisis Estadístico** 📊
   - Calcula producto más vendido
   - Calcula producto con mayor facturación
   - Calcula facturación por mes
   - Genera top 3 productos

5. **Persistencia en Base de Datos** 💾
   - Crea base de datos SQLite en `output/database/ventas.db`
   - Inserta todos los datos de ventas
   - Guarda resultados de análisis con timestamp

6. **Verificación con SQL** ✅
   - Ejecuta consulta SQL para verificar top 3 productos
   - Muestra resultados en consola

**Salida esperada:**
```
=== ANÁLISIS DE VENTAS ===

1. Cargando y limpiando datos...
Filas eliminadas en limpieza: 0
Datos limpios guardados en: data/processed/ventas_clean.csv
Datos procesados: 50 filas válidas

2. Realizando análisis...

Producto más vendido: Teclado (69 unidades)
Producto mayor facturación: Monitor ($2,539,400.00)

Facturación mensual:
  2023-01: $1,689,580.00
  2023-02: $1,859,410.00
  2023-03: $2,429,500.00
  ...

3. Guardando en base de datos...
Insertadas 50 filas en tabla ventas
Resultados de análisis guardados en BD

4. Verificando con consulta SQL - Top 3 productos:
  Teclado: 69 unidades
  Monitor: 60 unidades
  Impresora: 50 unidades

Proceso completado exitosamente!
- Datos limpios guardados en: data/processed/ventas_clean.csv
- Base de datos SQLite en: output/database/ventas.db
- Ejecuta 'python -m src.visualizer' para generar gráficos
- Ejecuta 'pytest' para correr las pruebas
```

### Opción 2: Generar Solo Gráficos

Si ya ejecutaste `main.py` y tienes la base de datos poblada:

```bash
python -m src.visualizer
```

**¿Qué hace este comando?**

1. Conecta a la base de datos SQLite
2. Obtiene datos de facturación mensual
3. Genera gráfico de barras (`output/graficos/grafico.png`)
4. Obtiene datos de top productos
5. Genera gráfico horizontal (`output/graficos/top_productos.png`)

**Salida esperada:**
```
Generando visualizaciones...
Gráfico guardado en: output/graficos/grafico.png
Gráfico de productos guardado en: output/graficos/top_productos.png
Visualizaciones completadas exitosamente!
```

**Características de los gráficos:**
- 📐 Resolución: 300 DPI (calidad impresión)
- 📏 Tamaño: 12×6 pulgadas (gráfico mensual)
- 🎨 Estilo: seaborn profesional
- 💰 Formato de valores: Incluye símbolos de moneda y separadores de miles
- 📊 Anotaciones: Valores directamente en las barras

### Opción 3: Usar Módulos Individualmente

**Ejemplo - Solo procesar datos:**
```python
from src.data_processor import DataProcessor

processor = DataProcessor()
processor.load_data("data/raw/ventas.csv")
processor.clean_data()
processor.calculate_totals()
df = processor.get_clean_data()

print(df.head())
print(f"Registros válidos: {len(df)}")
```

**Ejemplo - Solo análisis (sin BD):**
```python
import pandas as pd
from src.analyzer import SalesAnalyzer

# Cargar datos limpios
df = pd.read_csv("data/processed/ventas_clean.csv")
df['fecha'] = pd.to_datetime(df['fecha'])

# Crear analizador
analyzer = SalesAnalyzer(df)

# Obtener análisis específico
top_producto = analyzer.producto_mas_vendido()
print(f"Producto más vendido: {top_producto['producto']}")
print(f"Cantidad total: {top_producto['cantidad_total']}")

# Facturación mensual
facturacion = analyzer.facturacion_por_mes()
for mes, total in facturacion.items():
    print(f"{mes}: ${total:,.2f}")
```

**Ejemplo - Consultas SQL directas:**
```python
from src.database import DatabaseManager

db = DatabaseManager()

# Consulta personalizada
import pandas as pd
query = """
    SELECT producto, SUM(total) as ingresos_totales
    FROM ventas
    WHERE fecha >= '2023-01-01'
    GROUP BY producto
    ORDER BY ingresos_totales DESC
    LIMIT 5
"""

with db.get_connection() as conn:
    resultado = pd.read_sql_query(query, conn)
    print(resultado)
```

---

## 🧪 Ejecución de Tests

### ¿Por qué son importantes los tests?

Los tests automatizados garantizan que:
- ✅ Los cálculos matemáticos son correctos
- ✅ La limpieza de datos funciona como se espera
- ✅ Los cambios futuros no rompen funcionalidad existente
- ✅ El código es confiable para producción

### Ejecutar Todos los Tests

**Nota:** Asegúrate de tener pytest instalado:
```bash
pip install pytest
```

**Ejecutar tests:**
```bash
pytest
```

**Ejecutar con más detalles (verbose):**
```bash
pytest -v
```

**Ejecutar con reporte de cobertura:**
```bash
pytest --cov=src tests/
```

### Tests Incluidos

#### **Test 1: Cálculo de Totales**
```python
def test_calculate_totals():
    # Verifica que: total = cantidad × precio_unitario
    # Datos: 10 × 100 = 1000, 5 × 200 = 1000, 8 × 150 = 1200
    # Valida que los cálculos sean exactos
```

#### **Test 2: Limpieza de Datos**
```python
def test_clean_data_removes_negative_quantities():
    # Verifica que cantidades negativas sean eliminadas
    # Datos: [10, -5, 8] → [10, 8]
    # Valida que todas las cantidades resultantes > 0
```

#### **Test 3: Producto Más Vendido**
```python
def test_producto_mas_vendido():
    # Verifica identificación correcta del producto con más unidades
    # ProductoA: 10 + 15 = 25 unidades (ganador)
    # ProductoB: 5 unidades
    # ProductoC: 8 unidades
```

#### **Test 4: Mayor Facturación**
```python
def test_producto_mayor_facturacion():
    # Verifica producto con mayores ingresos totales
    # ProductoA: $1000 + $1500 = $2500 (ganador)
    # ProductoB: $1000
    # ProductoC: $1200
```

#### **Test 5: Facturación Mensual**
```python
def test_facturacion_por_mes():
    # Verifica agrupación y suma por mes
    # Enero: $2000, Febrero: $2700
    # Valida que no se modifique DataFrame original
```

#### **Test 6: Top Productos**
```python
def test_get_top_productos_cantidad():
    # Verifica ranking de productos por cantidad
    # Valida orden descendente y límite de resultados
```

### Salida Esperada de Tests

```
============================= test session starts ==============================
collected 6 items

tests/test_analyzer.py::TestDataProcessor::test_calculate_totals PASSED   [16%]
tests/test_analyzer.py::TestDataProcessor::test_clean_data_removes_negative_quantities PASSED [33%]
tests/test_analyzer.py::TestSalesAnalyzer::test_producto_mas_vendido PASSED [50%]
tests/test_analyzer.py::TestSalesAnalyzer::test_producto_mayor_facturacion PASSED [66%]
tests/test_analyzer.py::TestSalesAnalyzer::test_facturacion_por_mes PASSED [83%]
tests/test_analyzer.py::TestSalesAnalyzer::test_get_top_productos_cantidad PASSED [100%]

============================== 6 passed in 0.23s ===============================
```

---

## 🗄️ Uso de la Base de Datos SQLite

### Abrir y Explorar la Base de Datos

#### Opción 1: Extensión de VS Code
1. Instalar extensión **SQLite Viewer** (alexcvzz.vscode-sqlite)
2. Abrir archivo `output/database/ventas.db`
3. Explorar tablas visualmente

#### Opción 2: Cliente SQLite (DB Browser)
1. Descargar [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Abrir → `output/database/ventas.db`
3. Pestaña "Browse Data" para ver registros
4. Pestaña "Execute SQL" para consultas personalizadas

#### Opción 3: Desde Python
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('output/database/ventas.db')

# Ver todas las tablas
tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table'", 
    conn
)
print(tables)

# Ver contenido de tabla ventas
ventas = pd.read_sql_query("SELECT * FROM ventas LIMIT 10", conn)
print(ventas)

# Ver resultados de análisis
analisis = pd.read_sql_query("SELECT * FROM analisis_resultados", conn)
print(analisis)

conn.close()
```

### Esquema de la Base de Datos

#### Tabla: `ventas`
| Columna           | Tipo    | Descripción                   |
|-------------------|---------|-------------------------------|
| id                | INTEGER | Primary key autoincremental   |
| fecha             | DATE    | Fecha de la venta             |
| producto          | TEXT    | Nombre del producto           |
| cantidad          | INTEGER | Cantidad vendida              |
| precio_unitario   | REAL    | Precio por unidad             |
| total             | REAL    | Cantidad × precio_unitario    |

#### Tabla: `analisis_resultados`
| Columna          | Tipo      | Descripción                     |
|------------------|-----------|---------------------------------|
| id               | INTEGER   | Primary key autoincremental     |
| tipo_analisis    | TEXT      | Tipo de análisis realizado      |
| resultado        | TEXT      | Descripción del resultado       |
| valor            | REAL      | Valor numérico del resultado    |
| fecha_calculo    | TIMESTAMP | Fecha y hora del análisis       |

### Consultas SQL Útiles

Todas estas consultas están disponibles en `sql/queries.sql`:

#### 1. Top 3 Productos por Cantidad
```sql
SELECT 
    producto,
    SUM(cantidad) as cantidad_total
FROM ventas
GROUP BY producto
ORDER BY cantidad_total DESC
LIMIT 3;
```

#### 2. Facturación Mensual
```sql
SELECT 
    strftime('%Y-%m', fecha) as mes,
    SUM(total) as facturacion_total,
    COUNT(*) as numero_ventas
FROM ventas
GROUP BY strftime('%Y-%m', fecha)
ORDER BY mes;
```

#### 3. Resumen por Producto
```sql
SELECT 
    producto,
    SUM(cantidad) as cantidad_total,
    SUM(total) as facturacion_total,
    ROUND(AVG(precio_unitario), 2) as precio_promedio,
    COUNT(*) as numero_transacciones
FROM ventas
GROUP BY producto
ORDER BY facturacion_total DESC;
```

#### 4. Análisis de Crecimiento Mensual
```sql
WITH ventas_mensuales AS (
    SELECT 
        strftime('%Y-%m', fecha) as mes,
        SUM(total) as facturacion_total
    FROM ventas
    GROUP BY strftime('%Y-%m', fecha)
)
SELECT 
    mes,
    facturacion_total,
    LAG(facturacion_total) OVER (ORDER BY mes) as facturacion_anterior,
    ROUND(
        (facturacion_total - LAG(facturacion_total) OVER (ORDER BY mes)) / 
        LAG(facturacion_total) OVER (ORDER BY mes) * 100, 2
    ) as crecimiento_porcentual
FROM ventas_mensuales;
```

## 👨‍💻 Autor

**Leon Achata**  
Versión: 1.0.0  
Última actualización: Octubre 2025

---

**Happy Data Analysis! 📊✨**
