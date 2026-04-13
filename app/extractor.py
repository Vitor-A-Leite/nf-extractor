# Extrator dos textos das NFe
import pdfplumber
from openai import OpenAI
from app.models import NotaFiscal
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extrair_texto_pdf(caminho_pdf: str) -> str:
    """Extrai o texto bruto do PDF."""
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() or ""
    return texto

def extrair_dados_nf(caminho_pdf: str) -> NotaFiscal:
    """Pipeline completo: PDF → texto → LLM → Pydantic."""
    
    # 1. Extrai texto do PDF
    texto_bruto = extrair_texto_pdf(caminho_pdf)
    
    if not texto_bruto.strip():
        raise ValueError("Não foi possível extrair texto do PDF.")
    
    # 2. Monta o schema Pydantic como instrução pro LLM
    schema = NotaFiscal.model_json_schema()
    
    # 3. Chama a OpenAI com structured output
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # barato e suficiente pra extração
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um especialista em leitura de Notas Fiscais brasileiras. "
                    "Extraia APENAS os dados presentes no documento. "
                    "Responda SOMENTE com um JSON válido seguindo o schema fornecido. "
                    "Não inclua explicações, markdown ou texto adicional."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Extraia os dados desta Nota Fiscal e retorne um JSON "
                    f"seguindo exatamente este schema:\n\n{json.dumps(schema, ensure_ascii=False)}"
                    f"\n\nTexto da Nota Fiscal:\n\n{texto_bruto}"
                )
            }
        ],
        temperature=0,  # determinístico — importante pra extração
        response_format={"type": "json_object"}  # garante JSON válido
    )
    
    # 4. Parseia e valida com Pydantic
    dados_json = json.loads(response.choices[0].message.content)
    nota = NotaFiscal(**dados_json)  # Pydantic valida tipos automaticamente
    
    return nota