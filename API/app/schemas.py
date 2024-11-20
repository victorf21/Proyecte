from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Esquema per a Persona
class PersonaBase(BaseModel):
    nom: str
    cognom: str

class PersonaCreate(PersonaBase):
    pass

class PersonaResponse(PersonaBase):
    id: int

    class Config:
        orm_mode = True

# Esquema per a Marcatge
class MarcatgeBase(BaseModel):
    persona_id: int

class MarcatgeResponse(MarcatgeBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
