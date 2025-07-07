# 🎬 **CineForo - Foro de Películas**

Una plataforma web moderna para cinéfilos donde puedes escribir reseñas, comentar sobre películas y conectar con otros amantes del cine.

![Django](https://img.shields.io/badge/Django-5.2.3-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

## ✨ **Características**

### 🔐 **Autenticación de usuarios**
- ✅ Registro e inicio de sesión seguro
- ✅ Perfiles personalizables con biografía cinematográfica
- ✅ Configuraciones de privacidad (mostrar/ocultar información)

### 🎭 **Sistema de reseñas**
- ✅ Editor enriquecido con **CKEditor 5**
- ✅ Sistema de calificación con estrellas (1-5)
- ✅ **Sistema anti-spoilers** con blur/reveal
- ✅ Autocomplete inteligente para buscar películas

### 💬 **Comentarios y interacción**
- ✅ Comentarios anidados en reseñas
- ✅ Sistema de **likes** con AJAX
- ✅ Respuestas en tiempo real

### 🔍 **Búsqueda avanzada**
- ✅ Búsqueda de películas por título, director o género
- ✅ Filtros por calificación y categorías
- ✅ Resultados paginados

### 🎨 **Diseño moderno**
- ✅ **Responsive design** para móvil y desktop
- ✅ Interfaz intuitiva y atractiva
- ✅ Estadísticas en tiempo real
- ✅ Navegación contextual (oculta buscador en auth)

### ⚙️ **Panel administrativo**
- ✅ Gestión completa de películas y usuarios
- ✅ Moderación de contenido
- ✅ Dashboard con estadísticas

---

## 🚀 **Instalación**

### **Requisitos previos**
- Python 3.13+ 
- pip (incluido con Python)
- Git

### **1. Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/cineforo.git
cd cineforo
```

### **2. Crear entorno virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### **3. Instalar dependencias**
```bash
cd blog
pip install -r requirements.txt
```

### **4. Configurar variables de entorno**
```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar .env con tu configuración
# Cambiar SECRET_KEY por una clave segura
```

### **5. Configurar base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **6. Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

### **7. Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

🎉 **¡Listo!** Abre http://127.0.0.1:8000/ en tu navegador.

---

## 🏗️ **Arquitectura del proyecto**

```
InformatorioProyecto/
├── 📁 venv/                    # Entorno virtual
├── 📁 blog/                    # Proyecto Django principal
│   ├── 📄 manage.py            # CLI de Django
│   ├── 📄 requirements.txt     # Dependencias Python
│   ├── 📄 env.example          # Variables de entorno ejemplo
│   ├── 📁 blog/                # Configuración principal
│   │   ├── 📄 settings.py      # Configuración Django
│   │   └── 📄 urls.py          # URLs principales
│   ├── 📁 movies/              # Aplicación principal
│   │   ├── 📄 models.py        # Modelos de BD
│   │   ├── 📄 views.py         # Lógica de negocio
│   │   ├── 📄 urls.py          # Rutas de la app
│   │   ├── 📄 forms.py         # Formularios Django
│   │   └── 📄 admin.py         # Panel admin
│   ├── 📁 templates/           # Plantillas HTML
│   │   ├── 📄 base.html        # Template maestro
│   │   └── 📁 movies/          # Templates específicos
│   ├── 📁 static/              # Archivos estáticos
│   └── 📁 media/               # Uploads de usuarios
└── 📁 .vscode/                 # Configuración del editor
```

---

## 🛠️ **Tecnologías utilizadas**

### **Backend**
- **Django 5.2.3** - Framework web
- **SQLite** - Base de datos (desarrollo)
- **Python 3.13+** - Lenguaje principal

### **Frontend**
- **HTML5 + CSS3** - Estructura y estilos
- **JavaScript** - Interactividad (AJAX, spoilers)
- **CKEditor 5** - Editor de texto enriquecido
- **Font Awesome** - Iconografía

### **Funcionalidades**
- **Sistema de autenticación** completo
- **Gestión de archivos** (posters, avatars)
- **Búsqueda en tiempo real**
- **Responsive design**
- **Sistema anti-spoilers**

---

## 📋 **Uso**

### **Para usuarios normales:**
1. **Registrarse** o **iniciar sesión**
2. **Explorar películas** y leer reseñas
3. **Escribir reseñas** detalladas con formato
4. **Comentar** en reseñas de otros usuarios
5. **Dar likes** a contenido que te guste
6. **Personalizar perfil** con información cinematográfica

### **Para administradores:**
1. Acceder al **panel admin** en `/admin/`
2. **Gestionar películas** (agregar, editar, eliminar)
3. **Moderar contenido** de usuarios
4. **Ver estadísticas** del foro

---

## 🤝 **Contribuir**

¡Las contribuciones son bienvenidas! Por favor:

1. **Fork** el repositorio
2. Crea una **rama nueva** (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un **Pull Request**

---

## 📊 **Estado del proyecto**

### **✅ Completado**
- Sistema de autenticación
- CRUD de reseñas con CKEditor
- Sistema de comentarios
- Sistema anti-spoilers
- Búsqueda avanzada
- Panel administrativo
- Diseño responsive

### **🚧 En desarrollo**
- Sistema de notificaciones
- API REST
- Integración con TMDB
- Sistema de recomendaciones

### **📝 Futuras mejoras**
- Chat en tiempo real
- Sistema de valoraciones
- Exportar reseñas a PDF
- App móvil

---

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 **Autor**

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@gmail.com

---

## 🙏 **Agradecimientos**

- **Django** por el framework excepcional
- **CKEditor** por el editor de texto
- **Font Awesome** por los iconos
- **Comunidad de desarrolladores** por inspiración y ayuda

---

<div align="center">

**¿Te gusta el proyecto? ¡Dale una ⭐ en GitHub!**

[🐛 Reportar Bug](https://github.com/tu-usuario/cineforo/issues) · 
[💡 Solicitar Feature](https://github.com/tu-usuario/cineforo/issues) · 
[📖 Documentación](https://github.com/tu-usuario/cineforo/wiki)

</div> 