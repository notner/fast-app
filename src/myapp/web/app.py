from fastapi import FastAPI, Request

from myapp.lib.ctx import ctx_from_env
from myapp.web.routers import movie

# app = FastAPI(dependencies=[Depends(get_query_token)])

app = FastAPI()
app.include_router(movie.router)
app.state.context = ctx_from_env('test')


@app.get('/')
async def root(request: Request):
    results = 'Hello'
    return {'message': results}
