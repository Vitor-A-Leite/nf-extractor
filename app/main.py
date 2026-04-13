from fastapi import FastAPI
from app.routers import nfe

app = FastAPI(
    title="NF-e Extractor API",
    description="Extrai dados estruturados de Notas Fiscais em PDF usando IA.",
    version="1.0.0"
)

app.include_router(nfe.router)

@app.get("/")
def root():
    return {"message": "NF-e Extractor API está rodando."}