from fastapi import FastAPI
from app.routers import marcatges

app = FastAPI()

# Incloure els routers
app.include_router(marcatges.router)
