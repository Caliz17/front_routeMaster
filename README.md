# RouteMaster Frontend

Aplicación frontend en Flask que consume la API de autenticación y gestión de recursos de RouteMaster. Este proyecto implementa un panel administrativo con formularios completos para usuarios, productos, clientes, pedidos y rutas, integrando autenticación JWT, roles y permisos granulares.

## Requisitos

- Python 3.11+
- API de RouteMaster disponible (FastAPI) en `http://localhost:8000`
- Virtualenv recomendado

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Cree un archivo `.env` en la raíz con al menos:

```env
SECRET_KEY=alguna_clave_segura
API_BASE_URL=http://localhost:8000
APP_NAME=RouteMaster
```

## Ejecución

```bash
flask --app run.py --debug run
```

Accede a `http://localhost:5000` y autentícate con las credenciales existentes en la API.

## Estructura MVC

- **Controllers (`app/controllers`)**: Blueprints por módulo (auth, dashboard, usuarios, productos, clientes, pedidos, rutas).
- **Services (`app/services`)**: Cliente HTTP centralizado para consumir los endpoints externos.
- **Forms (`app/forms`)**: Formularios WTForms con validaciones para cada entidad.
- **Templates (`app/templates`)**: Vistas Jinja con componentes Bootstrap 5.
- **Models (`app/models`)**: Modelos ligeros para representar al usuario autenticado.

## Características clave

- Inicio de sesión, registro y cierre de sesión con JWT.
- Protección de vistas con `Flask-Login` y validación de permisos.
- Tablero moderno con métricas en tiempo real (consumidas desde la API).
- CRUD completo para productos, clientes, pedidos y rutas.
- Estilos modernos con Bootstrap 5 y personalización propia.

## Pruebas rápidas

Puede verificar la sintaxis del proyecto ejecutando:

```bash
python -m compileall app
```

Esto asegura que todos los módulos se compilan correctamente.
