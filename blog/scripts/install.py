#!/usr/bin/env python3
"""
Script de instalación automática para CineForo
Automatiza el proceso de configuración inicial del proyecto.
"""

import os
import sys
import subprocess
import shutil
import secrets
from pathlib import Path

def print_step(step, message):
    """Imprimir paso con formato."""
    print(f"\n🚀 PASO {step}: {message}")
    print("=" * 50)

def print_success(message):
    """Imprimir mensaje de éxito."""
    print(f"✅ {message}")

def print_error(message):
    """Imprimir mensaje de error."""
    print(f"❌ ERROR: {message}")

def print_warning(message):
    """Imprimir mensaje de advertencia."""
    print(f"⚠️  {message}")

def print_info(message):
    """Imprimir mensaje informativo."""
    print(f"ℹ️  {message}")

def run_command(command, check=True, capture_output=False):
    """Ejecutar comando del sistema."""
    print(f"Ejecutando: {command}")
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(command, shell=True, check=check)
            return result.returncode == 0, None, None
    except subprocess.CalledProcessError as e:
        return False, None, str(e)

def check_python_version():
    """Verificar versión de Python."""
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print_error("Se requiere Python 3.8 o superior")
        print(f"Versión actual: {python_version.major}.{python_version.minor}.{python_version.micro}")
        return False
    
    print_success(f"Python {python_version.major}.{python_version.minor}.{python_version.micro} detectado")
    return True

def check_pip():
    """Verificar que pip esté disponible."""
    success, stdout, stderr = run_command("pip --version", check=False, capture_output=True)
    if not success:
        print_error("pip no está instalado")
        print("💡 Instala pip desde: https://pip.pypa.io/en/stable/installation/")
        return False
    
    print_success("pip está disponible")
    return True

def check_git():
    """Verificar que git esté disponible."""
    success, stdout, stderr = run_command("git --version", check=False, capture_output=True)
    if not success:
        print_warning("git no está instalado")
        print("💡 Recomendamos instalar git para control de versiones")
        return False
    
    print_success("git está disponible")
    return True

def create_directories():
    """Crear directorios necesarios."""
    directories = [
        'static',
        'media',
        'media/posters',
        'media/avatars',
        'staticfiles',
        'scripts',
        'logs'
    ]
    
    created = []
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            created.append(directory)
    
    if created:
        print_success(f"Directorios creados: {', '.join(created)}")
    else:
        print_info("Todos los directorios ya existen")
    
    return True

def create_env_file():
    """Crear archivo .env con configuración."""
    if os.path.exists('.env'):
        print_info("Archivo .env ya existe")
        return True
    
    if not os.path.exists('env.example'):
        print_error("No se encontró env.example")
        return False
    
    # Copiar env.example a .env
    shutil.copy('env.example', '.env')
    
    # Generar SECRET_KEY automáticamente
    secret_key = secrets.token_urlsafe(50)
    
    # Leer el archivo .env
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar la SECRET_KEY por defecto
    content = content.replace(
        'SECRET_KEY=tu-clave-secreta-super-segura-aqui-CAMBIALA-OBLIGATORIO',
        f'SECRET_KEY={secret_key}'
    )
    
    # Escribir el archivo .env actualizado
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print_success("Archivo .env creado con SECRET_KEY generada automáticamente")
    return True

def install_dependencies():
    """Instalar dependencias Python."""
    if not os.path.exists('requirements.txt'):
        print_error("No se encontró requirements.txt")
        return False
    
    print("📦 Instalando dependencias...")
    success, stdout, stderr = run_command("pip install -r requirements.txt", check=False)
    
    if not success:
        print_error("No se pudieron instalar las dependencias")
        print("💡 Verifica que tengas permisos de escritura y conexión a internet")
        if stderr:
            print(f"Error: {stderr}")
        return False
    
    print_success("Dependencias instaladas correctamente")
    return True

def setup_database():
    """Configurar base de datos."""
    print("🗄️  Configurando base de datos...")
    
    # Hacer migraciones
    success, stdout, stderr = run_command("python manage.py makemigrations", check=False)
    if not success:
        print_error("No se pudieron crear las migraciones")
        if stderr:
            print(f"Error: {stderr}")
        return False
    
    # Aplicar migraciones
    success, stdout, stderr = run_command("python manage.py migrate", check=False)
    if not success:
        print_error("No se pudieron aplicar las migraciones")
        if stderr:
            print(f"Error: {stderr}")
        return False
    
    print_success("Base de datos configurada correctamente")
    return True

def collect_static_files():
    """Recolectar archivos estáticos."""
    print("📁 Recolectando archivos estáticos...")
    success, stdout, stderr = run_command("python manage.py collectstatic --noinput", check=False)
    
    if not success:
        print_warning("No se pudieron recolectar archivos estáticos")
        print("💡 Esto es normal si no hay archivos estáticos aún")
    else:
        print_success("Archivos estáticos recolectados")
    
    return True

def create_gitignore():
    """Crear archivo .gitignore si no existe."""
    if os.path.exists('.gitignore'):
        print_info("Archivo .gitignore ya existe")
        return True
    
    gitignore_content = """# Django
*.log
*.pot
*.pyc
__pycache__/
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment variables
.env
.env.local
.env.production

# Virtual environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Backup files
*.bak
backup_*.sqlite3

# Logs
logs/
*.log

# Temporary files
temp_*.py
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print_success("Archivo .gitignore creado")
    return True

def create_superuser_option():
    """Opción para crear superusuario."""
    print("\n👤 CREAR SUPERUSUARIO")
    print("=" * 30)
    
    create_super = input("¿Deseas crear un superusuario ahora? (y/N): ").lower()
    if create_super in ['y', 'yes', 's', 'si']:
        print("\n📝 Creando superusuario...")
        success, stdout, stderr = run_command("python manage.py createsuperuser", check=False)
        if success:
            print_success("Superusuario creado exitosamente")
        else:
            print_warning("No se pudo crear el superusuario")
    else:
        print_info("Puedes crear un superusuario más tarde con: python manage.py createsuperuser")



def run_health_check():
    """Ejecutar verificación de salud del proyecto."""
    print("\n🏥 VERIFICACIÓN FINAL")
    print("=" * 30)
    
    success, stdout, stderr = run_command("python scripts/dev_commands.py health", check=False)
    if not success:
        print_warning("No se pudo ejecutar la verificación de salud")

def print_final_instructions():
    """Mostrar instrucciones finales."""
    print("\n🎉 ¡INSTALACIÓN COMPLETADA!")
    print("=" * 50)
    print("🚀 Para iniciar el servidor de desarrollo:")
    print("   python manage.py runserver")
    print("\n🌐 Luego abre en tu navegador:")
    print("   http://127.0.0.1:8000/")
    print("\n⚙️  Panel de administración:")
    print("   http://127.0.0.1:8000/admin/")
    print("\n📋 Comandos útiles:")
    print("   python scripts/dev_commands.py help     # Ver comandos disponibles")
    print("   python scripts/dev_commands.py health   # Verificar salud del proyecto")
    print("   python manage.py createsuperuser        # Crear superusuario")
    print("\n📖 Documentación del proyecto:")
    print("   README.md - Información general")
    print("   env.example - Variables de entorno disponibles")

def main():
    """Función principal de instalación."""
    print("🎬 CINEFORO - INSTALADOR AUTOMÁTICO")
    print("====================================")
    print("Este script configurará automáticamente tu proyecto CineForo")
    print("Tiempo estimado: 2-3 minutos")
    
    # Verificar requisitos
    print_step(1, "Verificando requisitos del sistema")
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        sys.exit(1)
    
    check_git()  # Git es opcional
    
    # Crear directorios necesarios
    print_step(2, "Creando estructura de directorios")
    if not create_directories():
        sys.exit(1)
    
    # Instalar dependencias
    print_step(3, "Instalando dependencias Python")
    if not install_dependencies():
        sys.exit(1)
    
    # Configurar variables de entorno
    print_step(4, "Configurando variables de entorno")
    if not create_env_file():
        sys.exit(1)
    
    # Configurar base de datos
    print_step(5, "Configurando base de datos")
    if not setup_database():
        sys.exit(1)
    
    # Recolectar archivos estáticos
    print_step(6, "Configurando archivos estáticos")
    collect_static_files()
    
    # Crear .gitignore
    print_step(7, "Configurando control de versiones")
    create_gitignore()
    
    # Opciones adicionales
    create_superuser_option()
    
    # Verificación final
    run_health_check()
    
    # Instrucciones finales
    print_final_instructions()

if __name__ == "__main__":
    main() 