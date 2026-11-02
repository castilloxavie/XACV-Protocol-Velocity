# 🏎️ XACV Protocol Velocity

Juego de carreras arcade 2D desarrollado en Python con Tkinter, diseñado bajo estrictos estándares de Arquitectura de Software (3 Capas), Seguridad y Calidad ISO.

## 🛡️ Características Principales
- **Mecánica Arcade:** 4 carritos (1 jugador, 3 IA), sistema de 3 vidas, dificultad progresiva y puntuación en tiempo real.
- **Arquitectura de 3 Capas:** Separación estricta entre Presentación (`ui`), Lógica de Negocio (`logic`) y Acceso a Datos (`data`).
- **Base de Datos Blindada:** Persistencia al 100% mediante Procedimientos Almacenados (Stored Procedures) en MySQL.

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.12+
- **Interfaz Gráfica:** Tkinter + Pillow (PIL)
- **Base de Datos:** MySQL 8.0+ (InnoDB)
- **Seguridad:** Bcrypt, python-dotenv, mysql-connector-python (SSL/TLS).

## 🚀 Instalación y Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/castilloxavie/XACV-Protocol-Velocity.git
   cd XACV-Protocol-Velocity
   ```
---

2. **Crear y activar el entorno virtual**
    ```bash
    python -m venv .venv
   
    # En Windows:
    .venv\Scripts\activate
   
    # En Mac/Linux:
    source .venv/bin/activate
    ```
---

3. **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```
---

4. **Configurar la Base de Datos**
    
    Ejecuta los scripts SQL en tu gestor de MySQL (Workbench, DBeaver, etc.) estrictamente en el siguiente orden:

    *   `car_game.sql` ── Crea la base de datos y las tablas base.
    *   `car_gamer_store_procedure.sql` ── Crea los procedimientos almacenados (Stored Procedures).
    *   `car_game_permisos.sql` ── Crea el usuario de la aplicación con los permisos mínimos requeridos.

    Una vez creada la base de datos, configura las variables de entorno:
    1. Renombra el archivo `.env.example` a `.env`.
    2. Abre el archivo `.env` y coloca tus credenciales reales de MySQL.

---

5. **Ejecutar el juego**
    ```bash
    python main.py
    ```
---

## 📂 Estructura del Proyecto

```text
XACV-Protocol-Velocity/
├── 📂 assets/                  # Recursos estáticos del juego
│   └── 📂 car/                 # Sprites y texturas de los vehículos
│       ├── ia1.png
│       ├── ia2.png
│       ├── ia3.png
│       └── player.png
├── 📂 data/                    # Gestión y persistencia de datos (Python)
│   ├── __init__.py
│   ├── config.py               # Configuración centralizada del sistema
│   ├── database.py             # Conexión principal a la base de datos
│   └── user_repo.py            # Repositorio para la gestión de usuarios
├── 📂 databases/               # Scripts y esquemas de la base de datos SQL
│   ├── car_game.sql
│   ├── car_game_permisos.sql
│   ├── car_game_prueba_permisos.sql
│   └── car_gamer_store_procedure.sql
├── 📂 logic/                   # Lógica central y reglas del juego
│   ├── __init__.py
│   ├── auth.py                 # Módulo de autenticación y seguridad
│   └── game_engine.py          # Motor principal del juego
├── 📂 ui/                      # Capa de interfaz gráfica de usuario
│   ├── __init__.py
│   ├── game_view.py            # Pantalla y renderizado del juego
│   ├── login_view.py           # Pantalla de inicio de sesión
│   ├── register_view.py        # Pantalla de registro de usuarios
│   └── ui_manager.py           # Controlador central de las vistas
├── .env                        # Variables de entorno (Oculto/Privado)
├── .env.example                # Plantilla de ejemplo para variables de entorno
├── .gitignore                  # Archivos y carpetas excluidos de Git
├── main.py                     # Punto de entrada principal de la aplicación
├── README.md                   # Documentación del proyecto
└── requirements.txt            # Dependencias del proyecto Pip
```
## 👨‍💻 Autor
* **Xavier Alberto Castillo Varon** ── * Analista de Desarrollo  y Automatisación(RPA) de Software*

---

## ⚙️ Configuración del Entorno (`.env.example`)

El proyecto utiliza variables de entorno para gestionar las credenciales de forma segura. En la raíz del proyecto encontrarás el archivo `.env.example` con la siguiente estructura base:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=app_jugador
DB_PASSWORD=TuClaveAqui
DB_NAME=car_game_db
```

### Pasos para la configuración:
1. Copia o renombra el archivo `.env.example` como `.env`.
2. Reemplaza los valores por defecto con tus credenciales locales de MySQL.

   
   
   