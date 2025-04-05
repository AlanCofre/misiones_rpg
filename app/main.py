from fastapi import FastAPI
from app.routes import router
from app.database import init_db

app = FastAPI(
    title="Sistema de Misiones RPG",
    description="API REST que gestiona misiones tipo cola (FIFO) usando FastAPI y AQLAlchemy",
    version="1.0"
)

#Incluir rutas desde routers.py
app.include_router(router)

#inicializar base de datos al iniciar app
@app.on_event("startup")
def startup():
    init_db()