from typing import List, Optional, Any, Dict

# from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import Path
from fastapi import Query
from fastapi import Header

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends

from time import sleep

from models import Curso
from models import cursos


def fake_db():
    try:
        print('Abrindo conexão com banco de dados')
        sleep(1)
    finally:
        print('Fechando conexão com banco de dados')
        sleep(1)


app = FastAPI(title='Api do Renan', version='0.0.1', description='Serve para praticar')



@app.get('/cursos/', description='Retorna todos os cursos ou uma lista vazia', summary='Retorna todos os cursos', response_model=List[Curso], response_description='Cursos encontrados com sucesso')
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path(title='ID do curso', description='Deve ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = [curso for curso in cursos if curso.id == curso_id]
        return curso[0]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')


@app.post('/cursos/', status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_curso(curso: Curso):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(Curso)
    return curso


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um curso com id {curso_id}')
    

@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    try:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=204)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um curso com id {curso_id}')


# Query Parameters
@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), x_geek: str = Header(default=None), c: Optional[int] = None):
    soma = a + b
    if c:
        soma = soma + c

    print(f'X-GEEK: {x_geek}')

    return {'resultado': soma}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)
