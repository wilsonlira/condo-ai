from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import CondominioCreate, CondominioResponse
from models.models import Condominio

router = APIRouter(
    prefix="/condominios",
    tags=["Condominios"]
)

@router.post("/", response_model=CondominioResponse)
def criar_condominio(condominio: CondominioCreate, db: Session = Depends(get_db)):
    novo_condominio = Condominio(**condominio.dict())
    db.add(novo_condominio)
    db.commit()
    db.refresh(novo_condominio)
    return novo_condominio

@router.get("/", response_model=list[CondominioResponse])
def listar_condominios(db: Session = Depends(get_db)):
    return db.query(Condominio).all()
