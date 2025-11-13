from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select
import os
from contextlib import asynccontextmanager 

DATABASE_URL = os.getenv("DATABASE_URL")
engine = None

if DATABASE_URL:
    engine = create_engine(DATABASE_URL, echo=True)

def crear_db_y_tablas():
    if engine:
        SQLModel.metadata.create_all(engine)

# --- Modelos de Datos (Articulo, ArticuloCrear) ---
class Articulo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    precio: float
    descripcion: Optional[str] = None

class ArticuloCrear(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = None

# --- Dependencia de Sesión (obtener_sesion) ---
def obtener_sesion():
    if engine is None:
        raise Exception("El motor de la base de datos no está inicializado.")
    
    with Session(engine) as session:
        yield session

# --- Lifespan (reemplaza on_startup) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta ANTES de que la API empiece
    print("Iniciando API y creando tablas...")
    crear_db_y_tablas()
    yield
    # Código que se ejecuta DESPUÉS de que la API se detiene
    print("Cerrando API.")

# --- Crea la Aplicación ---
app = FastAPI(lifespan=lifespan) # <--- Pasa el lifespan 


# --- Endpoints (health, crear_articulo, leer_articulos) ---
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API funcionando"}

@app.post("/articulos/", response_model=Articulo)
def crear_articulo(articulo_data: ArticuloCrear, session: Session = Depends(obtener_sesion)):
    db_articulo = Articulo.model_validate(articulo_data)
    session.add(db_articulo)
    session.commit()
    session.refresh(db_articulo)
    return db_articulo

@app.get("/articulos/", response_model=List[Articulo])
def leer_articulos(session: Session = Depends(obtener_sesion)):
    articulos = session.exec(select(Articulo)).all()
    return articulos