import asyncio
import pandas as pd
import pathlib
import pickle
import zlib

from myapp.lib.ctx import AppCTX
from myapp.lib.const import UPDATE_MOVIE_DATA


# Read TSV file into DataFrame
# BLOCKING AND SLOW
def _get_movie_df_from_disk(ctx: AppCTX):
    title_info = pathlib.Path('./data/title.basics.tsv').resolve()
    df = pd.read_csv(
        title_info,
        delimiter='\t',
        index_col=['tconst'],
        # dtype={'isAdult': 'boolean', 'startYear': 'int', 'endYear': 'int'}
    )
    # Index? all the fun
    return df


async def populate_movie_db(ctx: AppCTX):
    loop = asyncio.get_running_loop()
    df = await loop.run_in_executor(None, _get_movie_df_from_disk, ctx)

    redis_cli = await ctx.redis
    await redis_cli.set(
        ctx.cfg['server']['redis']['imdb_title_basic_key'],
        zlib.compress(pickle.dumps(df))
    )

    # Publish a message out via Redis pub/sub to alert on new data
    await redis_cli.publish(UPDATE_MOVIE_DATA, 'New Data Available')


async def get_movies(ctx: AppCTX, limit=100):
    movie_df = await ctx.movie_df
    return movie_df.head(limit)


async def get_movie(ctx: AppCTX, title: str):
    movie_df = await ctx.movie_df
    movie = movie_df.loc[movie_df['originalTitle'] == title]
    return movie.head(1)
