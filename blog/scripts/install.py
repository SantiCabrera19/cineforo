#!/usr/bin/env python3
"""
Script de instalación automática para CineForo
Automatiza el proceso de configuración inicial del proyecto.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_step(step, message):
    """Imprimir paso con formato."""
    print(f"\n🚀 PASO {step}: {message}")
    print("=" * 50)

def run_command(command, check=True):
    """Ejecutar comando del sistema."""
    print(f"Ejecutando: {command}")
    result = subprocess.run(command, shell=True, check=check)
    return result.returncode == 0

def main():
    """Función principal de instalación."""
    print("🎬 CINEFORO - INSTALADOR AUTOMÁTICO")
    print("====================================\n")
    
    # Verificar Python
    print_step(1, "Verificando Python")
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ ERROR: Se requiere Python 3.8 o superior")
        sys.exit(1)
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} detectado")
    
    # Verificar pip
    print_step(2, "Verificando pip")
    if not run_command("pip --version", check=False):
        print("❌ ERROR: pip no está instalado")
        sys.exit(1)
    print("✅ pip está disponible")
    
    # Instalar dependencias
    print_step(3, "Instalando dependencias")
    if not run_command("pip install -r requirements.txt"):
        print("❌ ERROR: No se pudieron instalar las dependencias")
        sys.exit(1)
    print("✅ Dependencias instaladas correctamente")
    
    # Crear archivo .env si no existe
    print_step(4, "Configurando variables de entorno")
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            shutil.copy('env.example', '.env')
            print("✅ Archivo .env creado desde env.example")
            print("⚠️  IMPORTANTE: Edita .env con tu configuración")
        else:
            print("❌ WARNING: No se encontró env.example")
    else:
        print("✅ Archivo .env ya existe")
    
    # Migraciones
    print_step(5, "Configurando base de datos")
    if not run_command("python manage.py makemigrations"):
        print("❌ ERROR: No se pudieron crear las migraciones")
        sys.exit(1)
    
    if not run_command("python manage.py migrate"):
        print("❌ ERROR: No se pudieron aplicar las migraciones")
        sys.exit(1)
    print("✅ Base de datos configurada correctamente")
    
    # Collectstatic
    print_step(6, "Recolectando archivos estáticos")
    run_command("python manage.py collectstatic --noinput", check=False)
    print("✅ Archivos estáticos recolectados")
    
    # Crear superusuario
    print_step(7, "Crear superusuario (opcional)")
    create_super = input("¿Deseas crear un superusuario ahora? (y/N): ").lower()
    if create_super in ['y', 'yes', 's', 'si']:
        run_command("python manage.py createsuperuser", check=False)
    
    # Finalización
    print("\n🎉 ¡INSTALACIÓN COMPLETADA!")
    print("========================")
    print("Para iniciar el servidor:")
    print("  python manage.py runserver")
    print("\nLuego abre: http://127.0.0.1:8000/")
    print("\nPanel admin: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    main() 