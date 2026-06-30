import os
import django

from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from fastapi_app.routes import router

app = FastAPI(
    title="Sistema de Gestión Comercial y Ventas - FastAPI",
    description="API complementaria desarrollada con FastAPI para consultar productos, clientes y ventas.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    """Endpoint inicial de prueba."""
    return {
        "message": "API FastAPI del Sistema de Gestión Comercial y Ventas funcionando correctamente"
    }