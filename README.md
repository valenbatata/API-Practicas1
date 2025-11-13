Proyecto Final DevOps - API de Artículos
Este proyecto es la entrega final para la materia Aplicaciones Cloud Nativas del ITS Cipolletti.

El objetivo es una API mínima desarrollada con FastAPI que gestiona una lista de "Artículos". La aplicación está completamente contenerizada con Docker y se conecta a una base de datos PostgreSQL para persistir los datos.


El proyecto incluye pruebas automatizadas con Pytest y un flujo de Integración Continua (CI) con GitHub Actions que valida el código en cada push.


Tecnologías Utilizadas
API: FastAPI

Base de Datos: PostgreSQL

Contenerización: Docker & Docker Compose

ORM / Validación: SQLModel (combina Pydantic y SQLAlchemy)

Testing: Pytest

CI/CD: GitHub Actions

Ejecución en Local (Docker)
El requisito principal es que el proyecto se pueda ejecutar fácilmente en local con Docker.

Prerequisitos
Git

Docker

Docker Compose

Pasos para Ejecutar
Clonar el repositorio:

Bash

git clone https://github.com/valenbatata/API-Practicas1.git
cd API-Practicas1
Este único comando construirá la imagen de la API y levantará los contenedores de la API y la base de datos.

Bash

docker compose up --build
La API estará disponible en http://localhost:8000.

Para detener los servicios: Presiona Ctrl+C en la terminal donde se está ejecutando docker compose up. Para limpiar (eliminar los contenedores y la red), puedes ejecutar:

Bash

docker compose down

Pruebas (Testing)
El proyecto incluye un conjunto de pruebas automatizadas que validan los endpoints y la lógica de la API.

Ejecutar Pruebas Localmente
Puedes correr las pruebas en tu máquina local (recomendado antes de hacer un push).

Crear un entorno virtual:

Bash

python -m venv venv

Activar el entorno:

.\venv\Scripts\Activate


Instalar dependencias:

Bash

pip install -r requirements.txt


Ejecutar Pytest:

Bash

pytest


Integración Continua (CI)
El flujo de CI está configurado en .github/workflows/ci.yml. Este workflow se dispara automáticamente con cada push o pull request a la rama main  y ejecuta todas las pruebas de pytest.

Endpoints de la API
Puedes probar la API usando curl o una herramienta como Postman.

GET /health
Verifica el estado de salud de la API.

Bash

curl http://localhost:8000/health
Respuesta esperada:

JSON

{"status":"ok","message":"API funcionando"}
POST /articulos/
Crea un nuevo artículo. Requiere nombre y precio.


Bash

curl -X POST http://localhost:8000/articulos/ \
-H "Content-Type: application/json" \
-d '{"nombre": "Mouse Gamer", "precio": 4500.50, "descripcion": "Mouse con luces RGB"}'

Respuesta esperada:

JSON

{
  "nombre": "Mouse Gamer",
  "precio": 4500.50,
  "descripcion": "Mouse con luces RGB",
  "id": 1
}

GET /articulos/
Obtiene una lista de todos los artículos en la base de datos.

Bash

curl http://localhost:8000/articulos/

Respuesta esperada:

JSON

[
  {
    "nombre": "Mouse Gamer",
    "precio": 4500.50,
    "descripcion": "Mouse con luces RGB",
    "id": 1
  }
]