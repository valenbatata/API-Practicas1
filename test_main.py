import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool 
from main import app, obtener_sesion, Articulo

# --- Configuración de la Base de Datos de Prueba ---
DATABASE_URL_PRUEBA = "sqlite:///:memory:"

engine_prueba = create_engine(
    DATABASE_URL_PRUEBA, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool 
)


@pytest.fixture(name="client")
def client_fixture():
    # --- Setup (antes de la prueba) ---
    SQLModel.metadata.create_all(engine_prueba)
    
    with Session(engine_prueba) as session:
        
        def obtener_sesion_prueba():
            yield session

        app.dependency_overrides[obtener_sesion] = obtener_sesion_prueba
        

        with TestClient(app) as client:
            yield client

    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(engine_prueba)

# --- Pruebas (Tests) ---

def test_health_check(client: TestClient):
    """Prueba el endpoint /health"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API funcionando"}

def test_crear_y_leer_articulo(client: TestClient):
    """Prueba la creación (POST) y lectura (GET) de artículos"""
    
    response_post = client.post(
        "/articulos/",
        json={"nombre": "Teclado", "precio": 150.0, "descripcion": "Mecánico"}
    )
    
    assert response_post.status_code == 200
    data = response_post.json()
    assert data["nombre"] == "Teclado"
    assert data["precio"] == 150.0
    assert data["id"] is not None
    
    id_creado = data["id"]

  
    response_get = client.get("/articulos/")
    
    assert response_get.status_code == 200
    data_lista = response_get.json()
    
    assert isinstance(data_lista, list)
    assert len(data_lista) == 1
    assert data_lista[0]["nombre"] == "Teclado"
    assert data_lista[0]["id"] == id_creado

def test_validacion_error_422(client: TestClient):
    """Prueba que la API devuelve un error 422"""
    response = client.post(
        "/articulos/",
        json={"nombre": "Monitor sin precio"} 
    )
    assert response.status_code == 422