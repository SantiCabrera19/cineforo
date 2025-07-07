#!/usr/bin/env python3
"""
Comandos útiles para desarrollo - CineForo
Ejecutar con: python scripts/dev_commands.py [comando]
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

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
    
    # Eliminar migraciones (excepto __init__.py)
    migrations_dir = 'movies/migrations'
    if os.path.exists(migrations_dir):
        for file in os.listdir(migrations_dir):
            if file.endswith('.py') and file != '__init__.py':
                os.remove(os.path.join(migrations_dir, file))
        print("✅ Migraciones eliminadas")
    
    # Crear nuevas migraciones
    run_command("python manage.py makemigrations", "Creando nuevas migraciones")
    run_command("python manage.py migrate", "Aplicando migraciones")
    
    print("\n✅ Base de datos reseteada completamente")

def create_sample_data():
    """Crear datos de ejemplo para desarrollo."""
    print("\n📊 CREAR DATOS DE EJEMPLO")
    print("=" * 30)
    
    script = """
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from django.contrib.auth.models import User
from movies.models import Movie, Review, Comment, UserProfile
from datetime import date

# Crear usuarios de ejemplo
users_data = [
    {'username': 'cinefilos2024', 'email': 'cine@test.com', 'first_name': 'Ana', 'last_name': 'Cinéfila'},
    {'username': 'moviecritic', 'email': 'critic@test.com', 'first_name': 'Carlos', 'last_name': 'Crítico'},
    {'username': 'peliculero', 'email': 'peli@test.com', 'first_name': 'María', 'last_name': 'Peliculera'},
]

for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name']
        }
    )
    if created:
        user.set_password('test123')
        user.save()
        
        # Crear perfil
        UserProfile.objects.create(
            user=user,
            bio=f'Soy {user_data["first_name"]}, amante del cine desde siempre.',
            favorite_genre='Drama',
            birth_date=date(1990, 1, 1)
        )
        print(f'Usuario creado: {user.username}')

# Crear películas de ejemplo
movies_data = [
    {
        'title': 'Forrest Gump',
        'original_title': 'Forrest Gump',
        'year': 1994,
        'director': 'Robert Zemeckis',
        'genre': 'Drama',
        'duration': 142,
        'synopsis': 'La vida es como una caja de chocolates...',
        'imdb_rating': 8.8
    },
    {
        'title': 'Matrix',
        'original_title': 'The Matrix',
        'year': 1999,
        'director': 'Hermanas Wachowski',
        'genre': 'Ciencia Ficción',
        'duration': 136,
        'synopsis': 'Un programador descubre la realidad...',
        'imdb_rating': 8.7
    },
    {
        'title': 'El Padrino',
        'original_title': 'The Godfather',
        'year': 1972,
        'director': 'Francis Ford Coppola',
        'genre': 'Drama',
        'duration': 175,
        'synopsis': 'La saga de una familia mafiosa...',
        'imdb_rating': 9.2
    }
]

for movie_data in movies_data:
    movie, created = Movie.objects.get_or_create(
        title=movie_data['title'],
        year=movie_data['year'],
        defaults=movie_data
    )
    if created:
        print(f'Película creada: {movie.title}')

# Crear reseñas de ejemplo
if Movie.objects.exists() and User.objects.exists():
    movies = Movie.objects.all()
    users = User.objects.filter(username__in=['cinefilos2024', 'moviecritic'])
    
    reviews_data = [
        {
            'title': 'Una obra maestra atemporal',
            'content': '<p>Forrest Gump es una película que trasciende géneros y épocas. Tom Hanks ofrece una actuación memorable que nos hace reír y llorar.</p>',
            'rating': 5,
            'has_spoilers': False
        },
        {
            'title': 'Revolución cinematográfica',
            'content': '<p>Matrix cambió para siempre el cine de acción. Los efectos especiales eran innovadores para su época.</p><p><strong>Advertencia:</strong> Neo es el elegido.</p>',
            'rating': 4,
            'has_spoilers': True
        }
    ]
    
    for i, review_data in enumerate(reviews_data):
        if i < len(movies) and i < len(users):
            review, created = Review.objects.get_or_create(
                movie=movies[i],
                author=users[i],
                defaults=review_data
            )
            if created:
                print(f'Reseña creada: {review.title}')

print('\\n✅ Datos de ejemplo creados exitosamente')
print('Usuarios de prueba:')
print('- cinefilos2024 / test123')  
print('- moviecritic / test123')
print('- peliculero / test123')
"""
    
    # Ejecutar script
    with open('temp_sample_data.py', 'w', encoding='utf-8') as f:
        f.write(script)
    
    run_command("python temp_sample_data.py", "Creando datos de ejemplo")
    
    # Limpiar archivo temporal
    if os.path.exists('temp_sample_data.py'):
        os.remove('temp_sample_data.py')

def run_tests():
    """Ejecutar tests del proyecto."""
    run_command("python manage.py test", "Ejecutando tests")

def collect_static():
    """Recolectar archivos estáticos."""
    run_command("python manage.py collectstatic --noinput", "Recolectando archivos estáticos")

def create_superuser():
    """Crear superusuario interactivo."""
    run_command("python manage.py createsuperuser", "Crear superusuario")

def show_urls():
    """Mostrar todas las URLs del proyecto."""
    run_command("python manage.py show_urls", "Mostrando URLs del proyecto")

def backup_database():
    """Crear backup de la base de datos."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_db_{timestamp}.sqlite3"
    
    if os.path.exists('db.sqlite3'):
        import shutil
        shutil.copy('db.sqlite3', backup_name)
        print(f"✅ Backup creado: {backup_name}")
    else:
        print("❌ No se encontró db.sqlite3")

def main():
    """Función principal con argumentos."""
    parser = argparse.ArgumentParser(description='Comandos de desarrollo para CineForo')
    parser.add_argument('command', choices=[
        'reset-db', 'sample-data', 'test', 'collectstatic', 
        'superuser', 'urls', 'backup', 'help'
    ], help='Comando a ejecutar')
    
    args = parser.parse_args()
    
    print("🛠️  CINEFORO - HERRAMIENTAS DE DESARROLLO")
    print("=" * 45)
    
    if args.command == 'reset-db':
        reset_database()
    elif args.command == 'sample-data':
        create_sample_data()
    elif args.command == 'test':
        run_tests()
    elif args.command == 'collectstatic':
        collect_static()
    elif args.command == 'superuser':
        create_superuser()
    elif args.command == 'urls':
        show_urls()
    elif args.command == 'backup':
        backup_database()
    elif args.command == 'help':
        print("Comandos disponibles:")
        print("  reset-db     - Resetear base de datos completamente")
        print("  sample-data  - Crear datos de ejemplo")
        print("  test         - Ejecutar tests")
        print("  collectstatic- Recolectar archivos estáticos")
        print("  superuser    - Crear superusuario")
        print("  urls         - Mostrar URLs del proyecto")
        print("  backup       - Backup de base de datos")

if __name__ == "__main__":
    main() 