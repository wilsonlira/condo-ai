import logging
import json
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
import models.models as models
from routers import condominios, atas, comunicados, documentos, ia
from dotenv import load_dotenv

load_dotenv()
models.Base.metadata.create_all(bind=engine)

# Configuração de logging estruturado em JSON
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

app = FastAPI()

# Middleware de logging estruturado
@app.middleware("http")
async def log_requests(request: Request, call_next):
    trace_id = str(uuid.uuid4())  # Gera um identificador único para a requisição
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    log_data = {
        "trace_id": trace_id,
        "client": request.client.host,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "response_time": round(process_time, 2)
    }
    logger.info(json.dumps(log_data))
    return response

# Configuração do CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos routers
app.include_router(condominios.router)
app.include_router(atas.router)
app.include_router(comunicados.router)
app.include_router(documentos.router)
app.include_router(ia.router)
