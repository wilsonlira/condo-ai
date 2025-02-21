from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# ==========================
# Esquemas para Condomínio
# ==========================

class CondominioBase(BaseModel):
    nome: str
    endereco: str

class CondominioCreate(CondominioBase):
    pass

class CondominioResponse(CondominioBase):
    id: int

    class Config:
        orm_mode = True

class Condominio(CondominioBase):
    id: int

    class Config:
        from_attributes = True

# ==========================
# Esquemas para Atas
# ==========================

class AtaBase(BaseModel):
    titulo: str
    conteudo: str

class AtaCreate(AtaBase):
    condominio_id: int

class Ata(AtaBase):
    id: int
    condominio_id: int
    data_criacao: datetime

    class Config:
        from_attributes = True

class AtaResponse(AtaBase):
    id: int
    data_criacao: datetime
    condominio_nome: str  # Adiciona o nome do condomínio à resposta

    class Config:
        from_attributes = True

# ==========================
# Esquemas para Comunicados
# ==========================

class ComunicadoBase(BaseModel):
    titulo: str
    conteudo: str

class ComunicadoCreate(ComunicadoBase):
    condominio_id: int

class Comunicado(ComunicadoBase):
    id: int
    condominio_id: int
    data_criacao: datetime

    class Config:
        from_attributes = True

class ComunicadoResponse(ComunicadoBase):
    id: int
    data_criacao: datetime
    condominio_id: int
    condominio_nome: str

    class Config:
        from_attributes = True