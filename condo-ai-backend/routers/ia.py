from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.models import Ata, Comunicado
from typing import List
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carregar variáveis do ambiente
load_dotenv()

# Configurar a chave da OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("A chave da OpenAI não está configurada. Defina OPENAI_API_KEY nas variáveis de ambiente.")

# Inicializar cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

router = APIRouter(
    prefix="/ia",
    tags=["IA"]
)

class ConsultaIARequest(BaseModel):
    pergunta: str

@router.post("/consultar")
def consultar_ia(request: ConsultaIARequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request.pergunta}]
        )
        return {"resposta": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar IA: {str(e)}")

@router.get("/consulta")
def consultar_documentos(termo: str, db: Session = Depends(get_db)):
    """
    Consulta atas e comunicados com base em um termo e gera uma resposta usando IA.
    """
    atas = db.query(Ata).filter(Ata.conteudo.ilike(f"%{termo}%")).all()
    comunicados = db.query(Comunicado).filter(Comunicado.conteudo.ilike(f"%{termo}%")).all()

    if not atas and not comunicados:
        return {"resposta": "Nenhum documento relevante encontrado."}

    documentos = [ata.conteudo for ata in atas] + [comunicado.conteudo for comunicado in comunicados]
    resposta_ia = "Aqui vai a resposta da IA baseada nos documentos encontrados."

    return {"resposta": resposta_ia, "documentos_encontrados": documentos}
