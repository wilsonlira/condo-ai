from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models.models import Ata, Comunicado
from schemas import AtaResponse, ComunicadoResponse
from typing import List, Optional

router = APIRouter(
    prefix="/documentos",
    tags=["Documentos"]
)

@router.get("/consulta", response_model=List[dict])
def consultar_documentos(
    palavra_chave: Optional[str] = Query(None, description="Palavra-chave para busca"),
    data_inicio: Optional[str] = Query(None, description="Data de início no formato YYYY-MM-DD"),
    data_fim: Optional[str] = Query(None, description="Data de fim no formato YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    documentos = []

    # Consultar atas
    atas_query = db.query(Ata)
    if palavra_chave:
        atas_query = atas_query.filter(Ata.conteudo.ilike(f"%{palavra_chave}%"))
    if data_inicio:
        atas_query = atas_query.filter(Ata.data_criacao >= data_inicio)
    if data_fim:
        atas_query = atas_query.filter(Ata.data_criacao <= data_fim)
    atas = atas_query.all()

    for ata in atas:
        documentos.append({
            "tipo": "Ata",
            "titulo": ata.titulo,
            "conteudo": ata.conteudo,
            "data_criacao": ata.data_criacao
        })

    # Consultar comunicados
    comunicados_query = db.query(Comunicado)
    if palavra_chave:
        comunicados_query = comunicados_query.filter(Comunicado.conteudo.ilike(f"%{palavra_chave}%"))
    if data_inicio:
        comunicados_query = comunicados_query.filter(Comunicado.data_criacao >= data_inicio)
    if data_fim:
        comunicados_query = comunicados_query.filter(Comunicado.data_criacao <= data_fim)
    comunicados = comunicados_query.all()

    for comunicado in comunicados:
        documentos.append({
            "tipo": "Comunicado",
            "titulo": comunicado.titulo,
            "conteudo": comunicado.conteudo,
            "data_criacao": comunicado.data_criacao
        })

    return documentos
