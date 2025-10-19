-- Consultas SQL para análisis de ventas

-- 1. Top 3 productos más vendidos por cantidad
SELECT 
    producto,
    SUM(cantidad) as cantidad_total
FROM ventas
GROUP BY producto
ORDER BY cantidad_total DESC
LIMIT 3;

-- 2. Top 3 productos por facturación
SELECT 
    producto,
    SUM(total) as facturacion_total,
    ROUND(SUM(total), 2) as facturacion_formateada
FROM ventas
GROUP BY producto
ORDER BY facturacion_total DESC
LIMIT 3;

-- 3. Facturación mensual
SELECT 
    strftime('%Y-%m', fecha) as mes,
    SUM(total) as facturacion_total,
    COUNT(*) as numero_ventas,
    ROUND(AVG(total), 2) as venta_promedio
FROM ventas
GROUP BY strftime('%Y-%m', fecha)
ORDER BY mes;

-- 4. Resumen por producto (cantidad, facturación, precio promedio)
SELECT 
    producto,
    SUM(cantidad) as cantidad_total,
    SUM(total) as facturacion_total,
    ROUND(AVG(precio_unitario), 2) as precio_promedio,
    COUNT(*) as numero_transacciones
FROM ventas
GROUP BY producto
ORDER BY facturacion_total DESC;

-- 5. Ventas por día de la semana
SELECT 
    CASE strftime('%w', fecha)
        WHEN '0' THEN 'Domingo'
        WHEN '1' THEN 'Lunes'
        WHEN '2' THEN 'Martes'
        WHEN '3' THEN 'Miércoles'
        WHEN '4' THEN 'Jueves'
        WHEN '5' THEN 'Viernes'
        WHEN '6' THEN 'Sábado'
    END as dia_semana,
    SUM(total) as facturacion_total,
    COUNT(*) as numero_ventas
FROM ventas
GROUP BY strftime('%w', fecha)
ORDER BY facturacion_total DESC;

-- 6. Productos con ventas por encima del promedio
WITH promedio_ventas AS (
    SELECT AVG(total) as venta_promedio
    FROM ventas
)
SELECT 
    v.producto,
    v.total,
    p.venta_promedio,
    ROUND(v.total - p.venta_promedio, 2) as diferencia_promedio
FROM ventas v
CROSS JOIN promedio_ventas p
WHERE v.total > p.venta_promedio
ORDER BY v.total DESC;

-- 7. Análisis de crecimiento mensual
WITH ventas_mensuales AS (
    SELECT 
        strftime('%Y-%m', fecha) as mes,
        SUM(total) as facturacion_total
    FROM ventas
    GROUP BY strftime('%Y-%m', fecha)
    ORDER BY mes
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

-- 8. Resultados guardados del análisis
SELECT 
    tipo_analisis,
    resultado,
    valor,
    fecha_calculo
FROM analisis_resultados
ORDER BY fecha_calculo DESC;