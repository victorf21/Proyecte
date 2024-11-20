from pydantic import BaseModel
from typing import Optional

class Marcatge(BaseModel):
    id: int
    usuari_id: int
    data_entrada: str
    data_sortida: Optional[str] = None
    espai_id: int
    estat: str

class MarcatgeCreate(BaseModel):
    usuari_id: int
    data_entrada: str
    espai_id: int
    estat: str
