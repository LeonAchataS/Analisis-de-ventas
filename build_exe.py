"""
Script para generar el ejecutable standalone con PyInstaller.

Uso:
    python build_exe.py

Esto generará un ejecutable en la carpeta dist/
"""

import PyInstaller.__main__
import os
from pathlib import Path

# Directorio del proyecto
PROJECT_DIR = Path(__file__).parent

# Configuración del build
PyInstaller.__main__.run([
    str(PROJECT_DIR / 'app.py'),
    '--onefile',
    '--windowed',
    '--name=AnalizadorVentas',
    # '--icon=assets/icon.ico',  # Descomentar cuando tengas un icono
    '--add-data=src;src',
    '--hidden-import=pandas',
    '--hidden-import=matplotlib',
    '--hidden-import=seaborn',
    '--hidden-import=openpyxl',
    '--hidden-import=tkinter',
    '--clean',
    '--noconfirm',
])

print("\n" + "="*60)
print("✓ Build completado!")
print("="*60)
print(f"Ejecutable generado en: {PROJECT_DIR / 'dist' / 'AnalizadorVentas.exe'}")
print("\nPruébalo ejecutando:")
print("  .\\dist\\AnalizadorVentas.exe")
print("="*60)
