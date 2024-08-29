from pydantic import BaseModel
from enum import Enum

class Brand(str, Enum):
    nitro = "Nitro"
    saloman = "Saloman"  # Corrected spelling from 'saloman' to 'salomon'
    burton = "Burton"

class SnowBoard(BaseModel):
    id: int
    length: int
    color: str
    has_bindings: bool
    brand: Brand 
