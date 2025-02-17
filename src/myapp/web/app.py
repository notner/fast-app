from fastapi import FastAPI
from myapp.web.routers import movie

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()
app.include_router(movie.router)


@app.get('/')
async def root():
    return {'message': 'hello world'}
