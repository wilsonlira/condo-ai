from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Condominio(Base):
    __tablename__ = "condominios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    endereco = Column(String)  # Novo campo

    atas = relationship("Ata", back_populates="condominio")
    comunicados = relationship("Comunicado", back_populates="condominio")

class Ata(Base):
    __tablename__ = "atas"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"))
    titulo = Column(String, index=True)
    conteudo = Column(Text)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    condominio = relationship("Condominio", back_populates="atas")

class Comunicado(Base):
    __tablename__ = "comunicados"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"))
    titulo = Column(String, index=True)
    conteudo = Column(Text)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    condominio = relationship("Condominio", back_populates="comunicados")