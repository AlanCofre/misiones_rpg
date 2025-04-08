from fastapi import FastAPI
from app.routes import router
from app.database import init_db

app = FastAPI()

#Incluir rutas desde routers.py
app.include_router(router)

#inicializar base de datos al iniciar app
@app.on_event("startup")
def startup():
    init_db()