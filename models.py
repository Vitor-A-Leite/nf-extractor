# Modelos pydantic
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Item(BaseModel):
    descricao: str
    quantidade: float
    unidade: str
    valor_unitario: float
    valor_total: float

class NotaFiscal(BaseModel):
    numero: str = Field(description="Número da NF-e")
    serie: Optional[str] = None
    data_emissao: str = Field(description="Data de emissão no formato DD/MM/AAAA")
    
    # Emitente
    emitente_nome: str
    emitente_cnpj: str
    emitente_uf: str
    emitente_contato: Optional[str] = None

    # Destinatário
    destinatario_nome: str
    destinatario_cnpj_cpf: str
    destinatario_contato: Optional[str] = None
    
    # Valores
    valor_produtos: float
    valor_frete: float = 0.0
    valor_desconto: float = 0.0
    valor_total: float
    
    # Itens
    itens: list[Item]
    
    # Impostos
    valor_icms: Optional[float] = None
    valor_pis: Optional[float] = None
    valor_cofins: Optional[float] = None
    chave_acesso: Optional[str] = Field(None, description="Chave de acesso de 44 dígitos")