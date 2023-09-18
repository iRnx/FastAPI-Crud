from typing import Optional

from pydantic import BaseModel, validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int 

    @validator('titulo')
    def validar_titulo(cls, value: str) -> str:
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O titulo deve ter pelo menos 3 palavras.')
        if value.islower():
            raise ValueError('O título deve ser capitalizado.')
        
        return value
    

    @validator('aulas')
    def validar_aulas(cls, value: int) -> int:
        
        if value < 12:
            raise ValueError('As aulas não pode ser menor que 12.')
        
        return value
    

    @validator('horas')
    def validar_horas(cls, value: int) -> int:
        
        if value < 10:
            raise ValueError('As horas não pode ser menor que 10.')
        
        return value


cursos = [
    Curso(id=1, titulo='Programação para leigos', aulas=45, horas=24),
    Curso(id=2, titulo='Django Rest Framework', aulas=67, horas=74),
]

