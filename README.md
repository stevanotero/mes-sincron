# Micro MES - Sincrón Diseño Electrónico

Sistema de Manufacturing Execution System (MES) simplificado para el monitoreo y cálculo de eficiencia (OEE) de líneas de producción.

## Tecnologías utilizadas

- **Backend**: FastAPI (Python)
- **Base de datos**: PostgreSQL con SQL nativo (sin ORM)
- **Autenticación**: JWT (JSON Web Tokens)
- **Frontend**: React + Vite
- **Control de versiones**: Git + GitHub

## Funcionalidades

- Autenticación con JWT (login protegido)
- CRUD completo de líneas de producción
- Cálculo automático de OEE (Overall Equipment Effectiveness):
  - Disponibilidad
  - Rendimiento
  - Calidad
  - Clasificación (Inaceptable / Regular / Aceptable / Buena / Excelencia)
- Validaciones de datos (campos individuales y relaciones lógicas entre ellos)
- Manejo de errores estandarizado (validación, HTTP y errores generales)
- Interfaz web en React para login y gestión visual de líneas

## Endpoints de la API

| Método | Endpoint              | Descripción                  | Requiere token |
|--------|------------------------|-------------------------------|-----------------|
| POST   | `/api/auth/login`      | Iniciar sesión                | No              |
| POST   | `/api/lineas/`          | Crear nueva línea             | Sí              |
| GET    | `/api/lineas/`          | Listar todas las líneas + OEE | Sí              |
| GET    | `/api/lineas/{id}`      | Obtener una línea             | Sí              |
| PUT    | `/api/lineas/{id}`      | Actualizar línea              | Sí              |
| DELETE | `/api/lineas/{id}`      | Eliminar línea                | Sí              |

## Estructura del proyecto
micro_mes/

├── app/

│   ├── main.py              # Punto de entrada de la API

│   ├── config.py            # Variables de entorno

│   ├── db.py                 # Conexión a PostgreSQL

│   ├── models.py             # Modelos Pydantic con validaciones

│   ├── auth.py                # Lógica de autenticación JWT

│   ├── error_handlers.py     # Manejadores de errores

│   └── routes/

│       ├── lineas.py          # Endpoints de líneas de producción

│       └── auth.py            # Endpoint de login

├── frontend/

│   └── src/

│       ├── api/api.js         # Configuración de axios

│       ├── pages/             # Login y Dashboard

│       └── components/        # Formulario y ruta protegida

├── .env                       # Variables de entorno (no se sube a git)

├── .gitignore

├── requirements.txt

└── README.md

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/stevanotero/mes-sincron.git
cd mes-sincron
```

### 2. Configurar el Backend

Crear y activar un entorno virtual:

```bash
python -m venv venv
source venv/Scripts/activate    # Windows (Git Bash)
# venv\Scripts\activate         # Windows (CMD)
# source venv/bin/activate      # Linux/Mac
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido (ajustar a tu configuración local):
DB_HOST=localhost

DB_PORT=5432

DB_NAME=micro_mes

DB_USER=postgres

DB_PASSWORD=tu_contraseña
JWT_SECRET=una_clave_secreta_larga_y_aleatoria

JWT_ALGORITHM=HS256

Ejecutar el servidor:

```bash
uvicorn app.main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`
Documentación interactiva (Swagger): `http://127.0.0.1:8000/docs`

### 3. Configurar el Frontend

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

La aplicación queda disponible en `http://localhost:5173`

### 4. Credenciales de prueba
Usuario: admin

Contraseña: admin123

## Cálculo de OEE

| Indicador      | Fórmula                                                    |
|-----------------|-------------------------------------------------------------|
| Tiempo operativo | Tiempo planificado − Tiempo de paradas                     |
| Disponibilidad   | Tiempo operativo / Tiempo planificado                       |
| Rendimiento      | Unidades producidas / (Tiempo operativo × Capacidad teórica)|
| Calidad          | (Unidades producidas − Unidades defectuosas) / Unidades producidas |
| OEE              | Disponibilidad × Rendimiento × Calidad                       |

### Clasificación según OEE

| Rango        | Clasificación |
|---------------|----------------|
| < 65%          | Inaceptable    |
| 65% - 74%      | Regular        |
| 75% - 84%      | Aceptable      |
| 85% - 94%      | Buena          |
| ≥ 95%          | Excelencia     |

## Próximas mejoras

- Tests automatizados
- Despliegue con Docker
- Sistema de usuarios persistente en base de datos (actualmente usa un usuario de prueba en memoria)
## Configuración y restauración de la base de datos

### 1. Crear la base de datos

Desde `psql` o tu cliente de PostgreSQL preferido (pgAdmin, DBeaver, etc.):

```sql
CREATE DATABASE micro_mes;
```

### 2. Ejecutar el script de inicialización

El proyecto incluye un script SQL con la estructura completa de las tablas (`usuarios` y `lineas_produccion`), restricciones de integridad y un usuario de prueba.

Desde la terminal:

```bash
psql -U postgres -d micro_mes -f database/init.sql
```

Esto crea:
- La tabla `usuarios` (supervisores de planta)
- La tabla `lineas_produccion`, con llave foránea hacia `usuarios`
- Restricciones `CHECK` para evitar valores inválidos (capacidades negativas, estados no permitidos, etc.)
- Un usuario de prueba: `admin` / `admin123`

### 3. Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto apuntando a esa base de datos (ver sección "Configurar el Backend" más arriba).

## Estrategia de gestión de conexiones a la base de datos

El proyecto utiliza `psycopg` (driver nativo de PostgreSQL para Python) sin ORM.

La estrategia actual es **una conexión por petición** (*connection per request*):

- Cada endpoint que necesita acceder a la base de datos abre una conexión nueva con `get_connection()` al inicio de la función.
- Se ejecuta la consulta parametrizada correspondiente (usando `%s` como placeholders, nunca concatenando strings, para prevenir inyección SQL).
- Se cierra el cursor y la conexión explícitamente al finalizar (`cursor.close()` y `conn.close()`).

Esta estrategia es simple y suficiente para el alcance de esta prueba técnica. Para un entorno de producción con mayor volumen de tráfico concurrente, lo recomendable sería implementar un **pool de conexiones** (por ejemplo, usando `psycopg_pool.ConnectionPool` de la librería `psycopg`), de modo que las conexiones se reutilicen en vez de abrirse y cerrarse en cada petición, reduciendo la sobrecarga de establecer conexiones TCP nuevas constantemente con PostgreSQL.