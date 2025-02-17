from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from pydantic import BaseModel

from myapp.core.repo import movie

router = APIRouter()


class Movie(BaseModel):
    titleType: str
    originalTitle: str
    endYear: str
    genres: str


@router.get('/movies', tags=['movies'])
async def read_movies(request: Request) -> list[Movie]:
    ctx = request.app.state.context
    df = await movie.get_movies(ctx, limit=5)
    return df.to_dict('records')


@router.get('/movie/{title}', tags=['movies'])
async def read_movie(title: str, request: Request) -> Movie:
    ctx = request.app.state.context
    df = await movie.get_movie(ctx, title=title)
    record = df.to_dict('records')
    if not record:
        raise HTTPException(status_code=404, detail=f'{title} not found in db')
    return record[0]


@router.get('/movies/populate', tags=['movies'])
async def populate_movies(request: Request):
    ctx = request.app.state.context
    await movie.populate_movie_db(ctx)
    return 'good'
