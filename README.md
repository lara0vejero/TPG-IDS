# 📚 TPG – Introducción al Desarrollo de Software (2C2025)
## 📖 Plataforma de Intercambio de Libros entre Estudiantes

Este repositorio contiene el desarrollo completo del Trabajo Práctico Grupal de la materia Introducción al Desarrollo de Software (FIUBA – Cátedra Lanzillotta, 2° cuatrimestre 2025).

El proyecto propone una plataforma web y mobile diseñada para facilitar el intercambio de material bibliográfico entre estudiantes universitarios, promoviendo una comunidad colaborativa, accesible y sostenible.

---

# 🎯 Objetivo General

Crear un sistema que permita a los estudiantes:
- Intercambiar libros y apuntes de manera sencilla.
- Encontrar material para sus cursadas sin costos adicionales.
- Ofrecer libros que ya no utilicen.
- Reducir gastos y fomentar la reutilización.

---

## 👤 Gestión de Usuarios
- Registro con validación completa.
- Inicio de sesión seguro.
- Perfiles personales.

## 📚 Gestión de Libros
- Publicación de libros con título, autor, editorial, ISBN, temática e imagen.
- Listado de libros publicados.
- Administración de libros propios.

## 🔁 Sistema de Intercambio
- Solicitud de intercambio entre usuarios.
- Generación de códigos únicos.
- Seguimiento del estado del intercambio.

## 🌐 Frontend Web
- Interfaz moderna, intuitiva y responsive.
- Secciones: Inicio, Biblioteca, Funcionamiento, Contacto, Sobre Nosotros.
- Formularios conectados al backend via RestFull

## 🖥️ Backend REST
- API desarrollada con Flask.
- Endpoints para usuarios y libros.
- Hashing de contraseñas.
- Persistencia en MySQL.

## 📱 App Mobile (Kivy)
- Login y navegación básica.
- Prueba de concepto mobile incluida como bonus.

---

# 🏗️ Arquitectura del Sistema

Estructura general del repositorio:

TPG-IDS/
 ├── back/          → API REST (Flask)
 ├── front/         → Web con Flask Templates
 ├── mobile/        → App hecha con Kivy

Frontend y Backend corren separados:
- Frontend → http://localhost:5000
- Backend  → http://localhost:5002

---

# 📦 Dependencias Utilizadas

## 🟦 Backend (Flask)
- Flask
- Flask-CORS
- Flask-Session
- Flask-Mail
- mysql-connector-python
- python-dotenv
- Werkzeug
- Despliegue del backend en PythonAnywhere para pruebas online

---

## 🟩 Frontend (Flask Web)
- Flask
- Bootstrap
- JQuery
- Swiper.js
- Google Fonts
- Requests

---

## 🟧 Mobile (Kivy)
- Kivy
- KivyMD
- Requests

---

# 🚀 Cómo Ejecutar el Proyecto Localmente

## 1️⃣ Backend
cd back/src
python3 app.py

Disponible en:
http://localhost:5002

---

## 2️⃣ Frontend
cd front
python3 app.py

Disponible en:
http://localhost:5000

---

## 3️⃣ App Mobile
cd mobile/kivy_app
python3 main.py

---

# 🛢️ Base de Datos (MySQL)

### datos_usuario
- id
- nombre_usuario
- email_usuario
- contraseña_usuario (hash)
- telefono_usuario
- direccion_usuario
- dni_usuario

### libros
- id
- usuario_id
- título
- autor
- editorial
- ISBN
- temática
- imagen
- estado

### intercambio_libro
- id
- id_libro_solicitado
- id_libro_ofrecido
- id_usuario_solicitado
- id_usuario_ofrecido
- estado

Script SQL: back/src/init_db.sql

---

# 🧪 Pruebas Realizadas

- Validación de formularios del front.
- Requests al backend con respuestas OK y errores.
- Manejo de estados HTTP (400, 401, 404).
- Hashing y verificación de contraseñas.
- Testing de endpoints.
- Pruebas en mobile.

---

# 🔐 Buenas Prácticas Aplicadas

- Hash seguro de contraseñas.
- Separación estricta front/back.
- Blueprints.
- Variables de entorno (.env).
- Manejo correcto de CORS.
- Sanitización de datos.

---

# 🤝 Equipo de Desarrollo

- Abril Martinelli
- Lara Ovejero
