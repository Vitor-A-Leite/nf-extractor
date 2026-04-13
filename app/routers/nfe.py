from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.models import NotaFiscal
from app.extractor import extrair_dados_nf
from app.auth import verificar_api_key
import tempfile
import os

router = APIRouter(prefix="/nfe", tags=["NF-e"])

@router.post("/extrair", response_model=NotaFiscal, dependencies=[Depends(verificar_api_key)])
async def extrair_nota_fiscal(file: UploadFile = File(...)):
    """
    Recebe um PDF de Nota Fiscal e retorna os dados estruturados.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos.")

    # Salva o PDF temporariamente (pdfplumber precisa de um path)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        nota = extrair_dados_nf(tmp_path)
        return nota
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    finally:
        os.unlink(tmp_path)  # limpa o arquivo temporário


@router.get("/health")
def health_check():
    return {"status": "ok"}