# 🎬 **CineForo - Foro de Películas**

Una plataforma web moderna para cinéfilos donde puedes escribir reseñas, comentar sobre películas y conectar con otros amantes del cine.

![Django](https://img.shields.io/badge/Django-5.2.3-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

## ✨ **Características Principales**

### 🔐 **Sistema de Usuarios**
- ✅ Registro e inicio de sesión seguro
- ✅ Perfiles personalizables con biografía cinematográfica
- ✅ Configuraciones de privacidad (mostrar/ocultar información)
- ✅ Sistema de avatares personalizado

### 🎭 **Sistema de Reseñas**
- ✅ Editor enriquecido con **CKEditor 5**
- ✅ Sistema de calificación con estrellas (1-5)
- ✅ **Sistema anti-spoilers** con blur/reveal inteligente
- ✅ Autocomplete inteligente para buscar películas
- ✅ Previews inteligentes con filtros personalizados

### 💬 **Comentarios e Interacción**
- ✅ Comentarios anidados en reseñas
- ✅ Sistema de **likes** con AJAX en tiempo real
- ✅ Respuestas contextuales
- ✅ Manejo de spoilers en comentarios

### 🔍 **Búsqueda Avanzada**
- ✅ Búsqueda de películas por título, director o género
- ✅ Filtros por calificación y categorías
- ✅ Resultados paginados con optimización
- ✅ Búsqueda AJAX con autocomplete

### 🎨 **Diseño Moderno**
- ✅ **Responsive design** para móvil y desktop
- ✅ Interfaz intuitiva y atractiva
- ✅ Estadísticas en tiempo real
- ✅ Navegación contextual inteligente

### ⚙️ **Panel Administrativo**
- ✅ Gestión completa de películas y usuarios
- ✅ Moderación de contenido
- ✅ Dashboard con estadísticas avanzadas

---

## 🚀 **Instalación Rápida**

### **Opción 1: Instalación Automática (Recomendada)**

```bash
# 1. Clonar el repositorio
git clone https://github.com/SantiCabrera19/cineforo.git
cd cineforo

# 2. Instalación completa automática
python setup.py fresh
```

### **Opción 2: Instalación Manual**

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 2. Instalar dependencias
cd blog
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp env.example .env
# Editar .env con tu configuración

# 4. Configurar base de datos
python manage.py makemigrations
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Ejecutar servidor
python manage.py runserver
```

---

## 🎯 **Scripts de Automatización**

### **Script Maestro - setup.py**

```bash
python setup.py fresh    # Instalación completa desde cero
python setup.py dev      # Configuración para desarrollo
python setup.py prod     # Configuración para producción
python setup.py help     # Ayuda completa
```

### **Comandos de Desarrollo**

```bash
# Herramientas de desarrollo
python scripts/dev_commands.py help           # Ver todos los comandos
python scripts/dev_commands.py health         # Verificar salud del proyecto
python scripts/dev_commands.py reset-db       # Resetear base de datos
python scripts/dev_commands.py sample-data    # Crear datos de ejemplo
python scripts/dev_commands.py backup         # Crear backup de BD
python scripts/dev_commands.py urls           # Mostrar URLs del proyecto
```

### **Script de Instalación**

```bash
python scripts/install.py    # Instalación guiada paso a paso
```

---

## 📋 **Datos de Ejemplo**

El proyecto incluye datos de ejemplo para desarrollo:

### **Usuarios de Prueba**
- **Usuario**: `cinefilos2024` | **Contraseña**: `test123`
- **Usuario**: `moviecritic` | **Contraseña**: `test123`
- **Usuario**: `peliculero` | **Contraseña**: `test123`
- **Usuario**: `directorFan` | **Contraseña**: `test123`

### **Películas Incluidas**
- 🎬 Forrest Gump (1994)
- 🎬 Matrix (1999)
- 🎬 El Padrino (1972)
- 🎬 Pulp Fiction (1994)
- 🎬 Inception (2010)

### **Contenido de Ejemplo**
- ✅ Reseñas detalladas con HTML enriquecido
- ✅ Comentarios anidados
- ✅ Perfiles completos con biografías
- ✅ Ejemplos de manejo de spoilers

---

## 🏗️ **Arquitectura del Proyecto**

```
InformatorioProyecto/
├── 📁 blog/                    # Proyecto Django principal
│   ├── 📄 manage.py            # CLI de Django
│   ├── 📄 setup.py             # Script maestro de configuración
│   ├── 📄 requirements.txt     # Dependencias Python
│   ├── 📄 env.example          # Variables de entorno ejemplo
│   ├── 📄 .gitignore           # Archivos ignorados por Git
│   │
│   ├── 📁 blog/                # Configuración principal
│   │   ├── 📄 settings.py      # Configuración Django
│   │   ├── 📄 pythonanywhere_settings.py  # Config producción
│   │   ├── 📄 urls.py          # URLs principales
│   │   └── 📄 wsgi.py          # WSGI para deployment
│   │
│   ├── 📁 movies/              # Aplicación principal
│   │   ├── 📄 models.py        # Modelos de BD (5 modelos)
│   │   ├── 📄 views.py         # Lógica de negocio (15+ vistas)
│   │   ├── 📄 urls.py          # Rutas de la app
│   │   ├── 📄 forms.py         # Formularios Django
│   │   ├── 📄 admin.py         # Panel admin personalizado
│   │   └── 📁 templatetags/    # Filtros personalizados
│   │
│   ├── 📁 templates/           # Plantillas HTML
│   │   ├── 📄 base.html        # Template maestro
│   │   └── 📁 movies/          # Templates específicos
│   │       ├── 📄 movie_list.html
│   │       ├── 📄 movie_detail.html
│   │       ├── 📄 review_list.html
│   │       ├── 📄 create_review.html
│   │       └── 📁 auth/        # Templates de autenticación
│   │
│   ├── 📁 scripts/             # Scripts de automatización
│   │   ├── 📄 install.py       # Instalación automática
│   │   ├── 📄 dev_commands.py  # Comandos de desarrollo
│   │   └── 📄 sample_data.py   # Datos de ejemplo
│   │
│   ├── 📁 static/              # Archivos estáticos
│   ├── 📁 staticfiles/         # Archivos estáticos compilados
│   ├── 📁 media/               # Uploads de usuarios
│   │   ├── 📁 posters/         # Posters de películas
│   │   └── 📁 avatars/         # Avatares de usuarios
│   │
│   └── 📁 logs/                # Logs del sistema
│
├── 📁 venv/                    # Entorno virtual
└── 📄 README.md               # Documentación principal
```

---

## 🛠️ **Tecnologías Utilizadas**

### **Backend**
- **Django 5.2.3** - Framework web robusto
- **SQLite** - Base de datos para desarrollo
- **MySQL** - Base de datos para producción (PythonAnywhere)
- **Python 3.8+** - Lenguaje principal

### **Frontend**
- **HTML5 + CSS3** - Estructura y estilos modernos
- **JavaScript** - Interactividad (AJAX, anti-spoilers)
- **CKEditor 5** - Editor de texto enriquecido
- **Font Awesome** - Iconografía profesional

### **Herramientas de Desarrollo**
- **python-decouple** - Gestión de variables de entorno
- **Pillow** - Procesamiento de imágenes
- **Custom Template Tags** - Filtros personalizados
- **Django Admin** - Panel administrativo customizado

### **Deployment**
- **PythonAnywhere** - Configuración específica incluida
- **WhiteNoise** - Servir archivos estáticos
- **Gunicorn** - Servidor WSGI para producción

---

## 📊 **Modelos de Datos**

### **Movie** - Películas
```python
- title, original_title, year, director
- genre, duration, synopsis
- poster (ImageField)
- imdb_rating, slug, created_at
```

### **Review** - Reseñas
```python
- movie (ForeignKey), author (ForeignKey)
- title, content (rich text), rating (1-5)
- has_spoilers (boolean), slug
- created_at, updated_at
```

### **Comment** - Comentarios
```python
- review (ForeignKey), author (ForeignKey)
- content, has_spoilers
- parent (self-referencing for nested comments)
- created_at
```

### **Like** - Sistema de Likes
```python
- review (ForeignKey), user (ForeignKey)
- created_at
- unique_together constraint
```

### **UserProfile** - Perfiles de Usuario
```python
- user (OneToOneField), bio, avatar
- favorite_genre, location, birth_date
- show_email, show_age (privacy settings)
- created_at, updated_at
```

---

## 🎨 **Funcionalidades Destacadas**

### **Sistema Anti-Spoilers**
- Detección automática de contenido con spoilers
- Blur/reveal inteligente en previews
- Advertencias visuales claras
- Filtros personalizados para templates

### **Editor Enriquecido**
- CKEditor 5 completamente configurado
- Configuraciones específicas por tipo de contenido
- Soporte para negritas, cursivas, listas
- Placeholder contextual

### **Búsqueda Avanzada**
- Autocomplete AJAX para películas
- Filtros por género y calificación
- Paginación optimizada
- Búsqueda por título, director, género

### **Sistema de Perfiles**
- Biografías cinematográficas
- Configuraciones de privacidad
- Historial de reseñas
- Estadísticas personales

---

## 🚀 **Deployment**

### **Desarrollo Local**
```bash
python manage.py runserver
# Abrir http://127.0.0.1:8000/
```

### **Producción PythonAnywhere**
```bash
# Usar configuración específica
export DJANGO_SETTINGS_MODULE=blog.pythonanywhere_settings
python manage.py migrate
python manage.py collectstatic
```

### **Variables de Entorno**
```env
SECRET_KEY=tu-clave-secreta-generada-automaticamente
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
# Ver env.example para configuración completa
```

---

## 🤝 **Contribuir al Proyecto**

### **Para Colaboradores**

1. **Clonar y configurar**:
```bash
git clone https://github.com/SantiCabrera19/cineforo.git
cd cineforo
python setup.py fresh
```

2. **Crear rama de desarrollo**:
```bash
git checkout -b feature/nueva-funcionalidad
```

3. **Desarrollar y probar**:
```bash
python scripts/dev_commands.py health
python manage.py test
```

4. **Crear Pull Request**:
```bash
git add .
git commit -m "feat: nueva funcionalidad implementada"
git push origin feature/nueva-funcionalidad
```

### **Guías de Contribución**
- ✅ Seguir las convenciones de Django
- ✅ Escribir tests para nuevas funcionalidades
- ✅ Documentar cambios significativos
- ✅ Mantener compatibilidad con Python 3.8+

---

## 📊 **Estado del Proyecto**

### **✅ Completado**
- [x] Sistema de autenticación completo
- [x] CRUD de películas y reseñas
- [x] Sistema de comentarios anidados
- [x] Sistema anti-spoilers
- [x] Búsqueda avanzada con filtros
- [x] Panel administrativo customizado
- [x] Diseño responsive
- [x] Scripts de automatización
- [x] Configuración de producción
- [x] Datos de ejemplo
- [x] Documentación completa

### **🚧 Posibles Mejoras Futuras**
- [ ] Sistema de notificaciones
- [ ] API REST con Django REST Framework
- [ ] Integración con TMDB API
- [ ] Sistema de recomendaciones
- [ ] Chat en tiempo real
- [ ] App móvil
- [ ] Sistema de ratings avanzado
- [ ] Exportar reseñas a PDF

---

## 🎬 **Comandos Útiles**

### **Desarrollo**
```bash
python manage.py runserver              # Servidor desarrollo
python manage.py shell                  # Shell interactivo
python manage.py dbshell                # Shell de base de datos
python manage.py check                  # Verificar configuración
python scripts/dev_commands.py help     # Ver comandos disponibles
```

### **Base de Datos**
```bash
python manage.py makemigrations         # Crear migraciones
python manage.py migrate                # Aplicar migraciones
python manage.py showmigrations         # Ver estado migraciones
python scripts/dev_commands.py reset-db # Resetear BD completa
```

### **Usuarios**
```bash
python manage.py createsuperuser        # Crear admin
python manage.py changepassword user    # Cambiar contraseña
python scripts/dev_commands.py sample-data # Crear datos ejemplo
```

### **Archivos Estáticos**
```bash
python manage.py collectstatic          # Recolectar estáticos
python manage.py findstatic archivo.css # Encontrar archivo
```

---

## 🎯 **Casos de Uso**

### **Para Usuarios**
1. **Registrarse** en la plataforma
2. **Explorar películas** y leer reseñas
3. **Escribir reseñas** detalladas con formato
4. **Comentar** en reseñas de otros usuarios
5. **Dar likes** a contenido que te guste
6. **Personalizar perfil** con información cinematográfica
7. **Buscar películas** por diferentes criterios

### **Para Administradores**
1. **Gestionar contenido** desde el panel admin
2. **Moderar reseñas** y comentarios
3. **Agregar nuevas películas** al catálogo
4. **Ver estadísticas** de uso de la plataforma
5. **Gestionar usuarios** y permisos

### **Para Desarrolladores**
1. **Clonar y configurar** proyecto automáticamente
2. **Desarrollar nuevas funcionalidades**
3. **Ejecutar tests** y verificaciones
4. **Crear datos de ejemplo** para desarrollo
5. **Generar backups** de la base de datos

---

## 📞 **Soporte y Documentación**

### **Documentación**
- 📖 **README.md** - Guía principal (este archivo)
- 📋 **env.example** - Configuración de variables
- 🛠️ **scripts/dev_commands.py help** - Comandos desarrollo
- 📊 **models.py** - Documentación inline de modelos

### **Ayuda Rápida**
```bash
python setup.py help                    # Ayuda completa
python scripts/dev_commands.py help     # Comandos desarrollo
python scripts/install.py --help        # Opciones instalación
```

### **Troubleshooting**
```bash
python scripts/dev_commands.py health   # Verificar salud proyecto
python manage.py check                  # Verificar configuración
python scripts/dev_commands.py urls     # Ver URLs disponibles
```

---

## 🌟 **Características Técnicas**

### **Seguridad**
- ✅ Protección CSRF integrada
- ✅ Validación de formularios robusta
- ✅ Sanitización de HTML en contenido
- ✅ Configuración de producción segura
- ✅ Gestión segura de archivos subidos

### **Performance**
- ✅ Consultas optimizadas con `select_related`
- ✅ Paginación eficiente
- ✅ Caching de consultas frecuentes
- ✅ Compresión de archivos estáticos
- ✅ Optimización de imágenes

### **Escalabilidad**
- ✅ Arquitectura modular
- ✅ Separación de configuraciones
- ✅ Preparado para múltiples entornos
- ✅ Base sólida para extensiones

---

<div align="center">

## 🎬 **¡Disfruta de CineForo!**

**¿Te gusta el proyecto? ¡Dale una ⭐ en GitHub!**

[🐛 Reportar Bug](https://github.com/SantiCabrera19/cineforo/issues) · 
[💡 Solicitar Feature](https://github.com/SantiCabrer19/cineforo/issues) · 
[📖 Documentación](https://github.com/SantiCabrera19/cineforo/wiki)

---

**Desarrollado con ❤️ para la comunidad de cinéfilos**

</div> 
