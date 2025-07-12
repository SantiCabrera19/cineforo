#!/usr/bin/env python3
"""
Script maestro de configuración para CineForo
Este script orquesta todo el proceso de instalación y configuración.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def print_banner():
    """Mostrar banner de CineForo."""
    print("""
🎬 ========================================== 🎬
    CINEFORO - CONFIGURACIÓN AUTOMÁTICA
          Blog de Películas Django
🎬 ========================================== 🎬
""")

def print_step(step, total, message):
    """Mostrar progreso del paso."""
    print(f"\n📋 [{step}/{total}] {message}")
    print("-" * 50)

def run_script(script_path, *args):
    """Ejecutar un script Python."""
    cmd = [sys.executable, script_path] + list(args)
    print(f"🔧 Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode == 0

def check_requirements():
    """Verificar que los archivos necesarios existan."""
    required_files = [
        'scripts/install.py',
        'scripts/dev_commands.py',
        'manage.py',
        'requirements.txt',
        'env.example'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print("❌ Archivos faltantes:")
        for file in missing:
            print(f"   - {file}")
        return False
    
    print("✅ Todos los archivos necesarios encontrados")
    return True

def setup_fresh_install():
    """Instalación completa desde cero."""
    print_banner()
    print("🚀 INSTALACIÓN COMPLETA DESDE CERO")
    print("Este proceso incluye:")
    print("  • Verificación de requisitos")
    print("  • Instalación de dependencias")
    print("  • Configuración de base de datos")
    print("  • Creación de directorios")
    print("  • Configuración de archivos")
    print("  • Opciones para datos de ejemplo")
    print("  • Verificación final")
    print("\nTiempo estimado: 3-5 minutos\n")
    
    # Verificar requisitos
    print_step(1, 3, "Verificando requisitos")
    if not check_requirements():
        return False
    
    # Ejecutar instalación
    print_step(2, 3, "Ejecutando instalación automática")
    if not run_script('scripts/install.py'):
        print("❌ Error en la instalación")
        return False
    
    # Verificación final
    print_step(3, 3, "Verificación final del proyecto")
    run_script('scripts/dev_commands.py', 'health')
    
    print("\n🎉 ¡INSTALACIÓN COMPLETA EXITOSA!")
    print("🌟 Tu blog de películas CineForo está listo")
    return True

def setup_development():
    """Configuración para desarrollo."""
    print_banner()
    print("🛠️  CONFIGURACIÓN PARA DESARROLLO")
    print("Este proceso incluye:")
    print("  • Reset de base de datos")
    print("  • Creación de datos de ejemplo")
    print("  • Configuración de desarrollo")
    print("\nTiempo estimado: 1-2 minutos\n")
    
    # Verificar requisitos
    print_step(1, 4, "Verificando requisitos")
    if not check_requirements():
        return False
    
    # Reset de base de datos
    print_step(2, 4, "Reseteando base de datos")
    if not run_script('scripts/dev_commands.py', 'reset-db'):
        print("❌ Error al resetear base de datos")
        return False
    
    # Crear datos de ejemplo
    print_step(3, 4, "Creando datos de ejemplo")
    if not run_script('scripts/dev_commands.py', 'sample-data'):
        print("⚠️  Error al crear datos de ejemplo")
    
    # Verificación final
    print_step(4, 4, "Verificación final")
    run_script('scripts/dev_commands.py', 'health')
    
    print("\n🎉 ¡CONFIGURACIÓN DE DESARROLLO COMPLETA!")
    print("🚀 Ejecuta: python manage.py runserver")
    return True

def setup_production():
    """Configuración para producción."""
    print_banner()
    print("🏭 CONFIGURACIÓN PARA PRODUCCIÓN")
    print("Este proceso incluye:")
    print("  • Recolección de archivos estáticos")
    print("  • Aplicación de migraciones")
    print("  • Verificación de configuración")
    print("\nTiempo estimado: 1 minuto\n")
    
    # Verificar requisitos
    print_step(1, 4, "Verificando requisitos")
    if not check_requirements():
        return False
    
    # Migraciones
    print_step(2, 4, "Aplicando migraciones")
    if not run_script('scripts/dev_commands.py', 'migrate'):
        print("❌ Error en migraciones")
    
    # Archivos estáticos
    print_step(3, 4, "Recolectando archivos estáticos")
    if not run_script('scripts/dev_commands.py', 'collectstatic'):
        print("❌ Error en archivos estáticos")
    
    # Verificación final
    print_step(4, 4, "Verificación final")
    run_script('scripts/dev_commands.py', 'health')
    
    print("\n🎉 ¡CONFIGURACIÓN DE PRODUCCIÓN COMPLETA!")
    print("🌐 Tu aplicación está lista para producción")
    return True

def show_help():
    """Mostrar ayuda completa."""
    print_banner()
    print("📖 AYUDA - CINEFORO SETUP")
    print("=" * 50)
    print("\n🎯 MODOS DE CONFIGURACIÓN:")
    print("  fresh      - Instalación completa desde cero")
    print("  dev        - Configuración para desarrollo")
    print("  prod       - Configuración para producción")
    print("  help       - Mostrar esta ayuda")
    
    print("\n🔧 COMANDOS ADICIONALES:")
    print("  python scripts/install.py              - Solo instalación")
    print("  python scripts/dev_commands.py help    - Comandos de desarrollo")
    print("  python manage.py runserver             - Iniciar servidor")
    print("  python manage.py createsuperuser       - Crear admin")
    
    print("\n📋 FLUJO RECOMENDADO:")
    print("  1. python setup.py fresh    # Primera vez")
    print("  2. python manage.py runserver")
    print("  3. Abrir http://127.0.0.1:8000/")
    
    print("\n🎬 DATOS DE EJEMPLO:")
    print("  Usuarios: cinefilos2024, moviecritic, peliculero")
    print("  Contraseña: test123")
    print("  Incluye: películas, reseñas, perfiles")
    
    print("\n📁 ESTRUCTURA DEL PROYECTO:")
    print("  blog/")
    print("  ├── blog/           # Configuración Django")
    print("  ├── movies/         # App principal")
    print("  ├── templates/      # Plantillas HTML")
    print("  ├── static/         # Archivos estáticos")
    print("  ├── media/          # Uploads de usuarios")
    print("  ├── scripts/        # Scripts de utilidad")
    print("  ├── requirements.txt")
    print("  ├── env.example")
    print("  └── manage.py")
    
    print("\n🌟 CARACTERÍSTICAS:")
    print("  • Sistema de usuarios con perfiles")
    print("  • CRUD de películas y reseñas")
    print("  • Editor de texto enriquecido")
    print("  • Sistema anti-spoilers")
    print("  • Comentarios anidados")
    print("  • Sistema de likes con AJAX")
    print("  • Búsqueda avanzada")
    print("  • Panel administrativo")
    print("  • Responsive design")
    
    print("\n📞 SOPORTE:")
    print("  • README.md para documentación")
    print("  • env.example para configuración")
    print("  • scripts/dev_commands.py para desarrollo")

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='Script maestro de configuración para CineForo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python setup.py fresh    # Instalación completa
  python setup.py dev      # Configuración desarrollo
  python setup.py prod     # Configuración producción
  python setup.py help     # Mostrar ayuda completa
        """
    )
    
    parser.add_argument(
        'mode',
        choices=['fresh', 'dev', 'prod', 'help'],
        help='Modo de configuración'
    )
    
    args = parser.parse_args()
    
    # Cambiar al directorio del proyecto si es necesario
    if not os.path.exists('manage.py'):
        print("⚠️  Ejecutando desde directorio raíz del proyecto...")
        if os.path.exists('blog/manage.py'):
            os.chdir('blog')
        else:
            print("❌ No se encontró manage.py")
            print("💡 Ejecuta desde la carpeta del proyecto Django")
            return False
    
    # Ejecutar el modo seleccionado
    if args.mode == 'fresh':
        return setup_fresh_install()
    elif args.mode == 'dev':
        return setup_development()
    elif args.mode == 'prod':
        return setup_production()
    elif args.mode == 'help':
        show_help()
        return True
    
    return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1) 