from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from myapp.lib.ctx import ctx_from_env
from myapp.lib.exc import ServerNotReady
from myapp.web.routers import movie


# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()


@app.get('/')
async def root(request: Request):
    results = 'Hello'
    return {'message': results}


def setup_app(env: str):
    app.include_router(movie.router)
    ctx = ctx_from_env(env)
    app.state.context = ctx

    @app.exception_handler(ServerNotReady)
    async def http_exception_handler(request, exc) -> JSONResponse:
        return JSONResponse(content={'error': str(exc)}, status_code=404)


# The magic is here.
setup_app('test')
###################
