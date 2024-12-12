from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import usuarios, aulas, modulo, ciclo, fecha, pertenecer, cursar, pasar_lista
# python -m uvicorn app.main:app --reload
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(usuarios.router)
app.include_router(aulas.router)
app.include_router(ciclo.router)
app.include_router(cursar.router)
app.include_router(fecha.router)
app.include_router(modulo.router)
app.include_router(pasar_lista.router)
app.include_router(pertenecer.router)

@app.get("/")
def read_root():
    return {"message": "Hola"}