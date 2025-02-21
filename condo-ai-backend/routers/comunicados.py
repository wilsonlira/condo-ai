from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import ComunicadoCreate, ComunicadoResponse
from models.models import Comunicado, Condominio

router = APIRouter(
    prefix="/comunicados",
    tags=["Comunicados"]
)

@router.post("/", response_model=ComunicadoResponse)
def criar_comunicado(comunicado: ComunicadoCreate, db: Session = Depends(get_db)):
    condominio = db.query(Condominio).filter(Condominio.id == comunicado.condominio_id).first()
    if not condominio:
        raise HTTPException(status_code=404, detail="Condomínio não encontrado")

    novo_comunicado = Comunicado(**comunicado.model_dump())
    db.add(novo_comunicado)
    db.commit()
    db.refresh(novo_comunicado)
    return ComunicadoResponse(
        id=novo_comunicado.id,
        titulo=novo_comunicado.titulo,
        conteudo=novo_comunicado.conteudo,
        data_criacao=novo_comunicado.data_criacao,
        condominio_id=comunicado.condominio_id,
        condominio_nome=condominio.nome
    )

@router.get("/", response_model=list[ComunicadoResponse])
def listar_comunicados(db: Session = Depends(get_db)):
    comunicados = db.query(Comunicado).join(Condominio).all()

    return [
        ComunicadoResponse(
            id=comunicado.id,
            titulo=comunicado.titulo,
            conteudo=comunicado.conteudo,
            data_criacao=comunicado.data_criacao,
            condominio_id=comunicado.condominio.id,  # 🔥 Adicionando condominio_id
            condominio_nome=comunicado.condominio.nome
        )
        for comunicado in comunicados
    ]


@router.put("/{comunicado_id}", response_model=ComunicadoResponse)
def atualizar_comunicado(comunicado_id: int, comunicado: ComunicadoCreate, db: Session = Depends(get_db)):
    comunicado_existente = db.query(Comunicado).filter(Comunicado.id == comunicado_id).first()
    if not comunicado_existente:
        raise HTTPException(status_code=404, detail="Comunicado não encontrado")

    # Atualiza os dados do comunicado
    comunicado_existente.titulo = comunicado.titulo
    comunicado_existente.conteudo = comunicado.conteudo
    comunicado_existente.condominio_id = comunicado.condominio_id  # Corrigido para incluir condominio_id

    # Busca o nome do condomínio atualizado
    condominio = db.query(Condominio).filter(Condominio.id == comunicado.condominio_id).first()
    if not condominio:
        raise HTTPException(status_code=404, detail="Condomínio não encontrado")

    db.commit()
    db.refresh(comunicado_existente)

    return ComunicadoResponse(
        id=comunicado_existente.id,
        titulo=comunicado_existente.titulo,
        conteudo=comunicado_existente.conteudo,
        data_criacao=comunicado_existente.data_criacao,
        condominio_id=comunicado_existente.condominio_id,  # Adiciona o campo esperado
        condominio_nome=condominio.nome
    )

@router.delete("/{comunicado_id}")
def deletar_comunicado(comunicado_id: int, db: Session = Depends(get_db)):
    comunicado = db.query(Comunicado).filter(Comunicado.id == comunicado_id).first()
    if not comunicado:
        raise HTTPException(status_code=404, detail="Comunicado não encontrado")

    db.delete(comunicado)
    db.commit()
    return {"detail": "Comunicado excluído com sucesso"}
