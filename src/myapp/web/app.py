import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from myapp.lib.ctx import ctx_from_env
from myapp.lib.exc import ServerNotReady
from myapp.lib.redis_ import reader
from myapp.web.routers import movie

from myapp.lib.const import UPDATE_MOVIE_DATA


async def redis_listeners(ctx):
    redis_cli = await ctx.redis

    # Subscribe to data changes so we can expire movie_df
    async with redis_cli.client().pubsub() as pubsub:
        await pubsub.subscribe(UPDATE_MOVIE_DATA)
        await asyncio.gather(reader(pubsub, ctx.expire_movie_df))


@asynccontextmanager
async def setup_app(app):
    app.include_router(movie.router)
    ctx = ctx_from_env('test')
    app.state.context = ctx

    @app.exception_handler(ServerNotReady)
    async def http_exception_handler(request, exc) -> JSONResponse:
        return JSONResponse(content={'error': str(exc)}, status_code=404)

    # Create tasks for Listeners
    asyncio.create_task(redis_listeners(ctx))

    yield

    # cleanup

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI(lifespan=setup_app)


@app.get('/')
async def root(request: Request):
    results = 'Hello'
    return {'message': results}
