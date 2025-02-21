from sqlalchemy.orm import Session
from models.models import Condominio, Ata, Comunicado

def create_condominio(db: Session, nome: str):
    db_condominio = Condominio(nome=nome)
    db.add(db_condominio)
    db.commit()
    db.refresh(db_condominio)
    return db_condominio

def get_condominios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Condominio).offset(skip).limit(limit).all()

def get_condominio_by_name(db: Session, nome: str):
    return db.query(Condominio).filter(Condominio.nome == nome).first()

# Criar uma ata
def create_ata(db: Session, titulo: str, conteudo: str, condominio_id: int):
    db_ata = Ata(titulo=titulo, conteudo=conteudo, condominio_id=condominio_id)
    db.add(db_ata)
    db.commit()
    db.refresh(db_ata)
    return db_ata
    
# Listar atas de um condomínio
def get_atas(db: Session, condominio_id: int):
    return db.query(Ata).filter(Ata.condominio_id == condominio_id).all()

# Criar um comunicado
def create_comunicado(db: Session, titulo: str, conteudo: str, condominio_id: int):
    db_comunicado = Comunicado(titulo=titulo, conteudo=conteudo, condominio_id=condominio_id)
    db.add(db_comunicado)
    db.commit()
    db.refresh(db_comunicado)
    return db_comunicado

# Listar comunicados de um condomínio
def get_comunicados(db: Session, condominio_id: int):
    return db.query(Comunicado).filter(Comunicado.condominio_id == condominio_id).all()