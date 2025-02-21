from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import AtaCreate, AtaResponse
from models.models import Ata, Condominio

router = APIRouter(
    prefix="/atas",
    tags=["Atas"]
)

@router.post("/", response_model=AtaResponse)
def criar_ata(ata: AtaCreate, db: Session = Depends(get_db)):
    condominio = db.query(Condominio).filter(Condominio.id == ata.condominio_id).first()
    if not condominio:
        raise HTTPException(status_code=404, detail="Condomínio não encontrado")

    nova_ata = Ata(**ata.model_dump())
    db.add(nova_ata)
    db.commit()
    db.refresh(nova_ata)
    return AtaResponse(
        id=nova_ata.id,
        titulo=nova_ata.titulo,
        conteudo=nova_ata.conteudo,
        data_criacao=nova_ata.data_criacao,
        condominio_id=ata.condominio_id,
        condominio_nome=condominio.nome
    )

@router.get("/", response_model=list[AtaResponse])
def listar_atas(db: Session = Depends(get_db)):
    atas = db.query(Ata).join(Condominio).all()
    return [
        AtaResponse(
            id=ata.id,
            titulo=ata.titulo,
            conteudo=ata.conteudo,
            data_criacao=ata.data_criacao,
            condominio_id=ata.condominio.id,
            condominio_nome=ata.condominio.nome
        )
        for ata in atas
    ]

@router.put("/{ata_id}", response_model=AtaResponse)
def atualizar_ata(ata_id: int, ata: AtaCreate, db: Session = Depends(get_db)):
    ata_existente = db.query(Ata).filter(Ata.id == ata_id).first()
    if not ata_existente:
        raise HTTPException(status_code=404, detail="Ata não encontrada")

    ata_existente.titulo = ata.titulo
    ata_existente.conteudo = ata.conteudo
    ata_existente.condominio_id = ata.condominio_id

    condominio = db.query(Condominio).filter(Condominio.id == ata.condominio_id).first()
    if not condominio:
        raise HTTPException(status_code=404, detail="Condomínio não encontrado")

    db.commit()
    db.refresh(ata_existente)
    return AtaResponse(
        id=ata_existente.id,
        titulo=ata_existente.titulo,
        conteudo=ata_existente.conteudo,
        data_criacao=ata_existente.data_criacao,
        condominio_id=ata.condominio_id,
        condominio_nome=condominio.nome
    )

@router.delete("/{ata_id}")
def deletar_ata(ata_id: int, db: Session = Depends(get_db)):
    ata = db.query(Ata).filter(Ata.id == ata_id).first()
    if not ata:
        raise HTTPException(status_code=404, detail="Ata não encontrada")

    db.delete(ata)
    db.commit()
    return {"detail": "Ata excluída com sucesso"}