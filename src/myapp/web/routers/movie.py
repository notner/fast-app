from fastapi import APIRouter

router = APIRouter()


@router.get('/movies/', tags=['movies'])
async def read_movies():
    return [{"name": "LOTR"}, {"name": "Avatar"}]
