#!/usr/bin/env python3
"""
Comandos de desarrollo básicos para CineForo
Solo comandos esenciales para el instalador
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

def check_django_project():
    """Verificar que estamos en un proyecto Django."""
    if not os.path.exists('manage.py'):
        print("❌ Error: No se encontró manage.py")
        print("💡 Ejecuta este script desde la carpeta del proyecto Django")
        sys.exit(1)

def run_command(command, description=None):
    """Ejecutar comando con descripción."""
    if description:
        print(f"\n🔧 {description}")
        print("-" * 40)
    
    print(f"Ejecutando: {command}")
    result = subprocess.run(command, shell=True)
    
    if result.returncode == 0:
        print("✅ Comando ejecutado exitosamente")
    else:
        print("❌ Error al ejecutar comando")
    
    return result.returncode == 0

def reset_database():
    """Resetear completamente la base de datos."""
    print("\n🗃️ RESETEAR BASE DE DATOS")
    print("=" * 30)
    
    confirm = input("⚠️  Esto eliminará TODOS los datos. ¿Continuar? (y/N): ")
    if confirm.lower() not in ['y', 'yes', 's', 'si']:
        print("Operación cancelada.")
        return
    
    # Eliminar base de datos
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("✅ Base de datos eliminada")
    
    # Crear nuevas migraciones
    run_command("python manage.py makemigrations", "Creando migraciones")
    run_command("python manage.py migrate", "Aplicando migraciones")
    
    print("\n✅ Base de datos reseteada completamente")

def check_project_health():
    """Verificar salud del proyecto."""
    print("\n🏥 VERIFICACIÓN DE SALUD DEL PROYECTO")
    print("=" * 45)
    
    # Verificar archivos críticos
    critical_files = [
        'manage.py',
        'requirements.txt',
        'env.example',
        'movies/models.py',
        'movies/views.py',
        'templates/base.html'
    ]
    
    print("\n📁 Archivos críticos:")
    for file in critical_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - FALTANTE")
    
    # Verificar directorios
    critical_dirs = [
        'static',
        'media',
        'templates',
        'movies/migrations'
    ]
    
    print("\n📂 Directorios críticos:")
    for dir in critical_dirs:
        if os.path.exists(dir):
            print(f"  ✅ {dir}/")
        else:
            print(f"  ❌ {dir}/ - FALTANTE")
    
    # Verificar configuración
    print("\n⚙️ Configuración:")
    if os.path.exists('.env'):
        print("  ✅ .env encontrado")
    else:
        print("  ⚠️  .env no encontrado (usa env.example)")
    
    print("\n🔧 Comandos sugeridos:")
    print("  python manage.py check           # Verificar configuración Django")
    print("  python manage.py makemigrations  # Crear migraciones")
    print("  python manage.py migrate         # Aplicar migraciones")

def main():
    """Función principal con argumentos."""
    parser = argparse.ArgumentParser(description='Comandos de desarrollo básicos para CineForo')
    parser.add_argument('command', choices=[
        'reset-db', 'health', 'help'
    ], help='Comando a ejecutar')
    
    args = parser.parse_args()
    
    print("🛠️  CINEFORO - HERRAMIENTAS BÁSICAS")
    print("=" * 40)
    
    # Verificar que estamos en el directorio correcto
    check_django_project()
    
    if args.command == 'reset-db':
        reset_database()
    elif args.command == 'health':
        check_project_health()
    elif args.command == 'help':
        print("\n📋 Comandos disponibles:")
        print("  reset-db           - Resetear base de datos completamente")
        print("  health             - Verificar salud del proyecto")
        print("  help               - Mostrar esta ayuda")
        
        print("\n💡 Ejemplos de uso:")
        print("  python scripts/dev_commands.py reset-db")
        print("  python scripts/dev_commands.py health")

if __name__ == "__main__":
    main() 