import pathlib
import pandas as pd
import pickle
import zlib

from myapp.lib.ctx import AppCTX


# Read TSV file into DataFrame
def _get_movie_df_from_disk(ctx: AppCTX):
    title_info = pathlib.Path('./data/title.basics.tsv').resolve()
    df = pd.read_csv(
        title_info,
        delimiter='\t',
        index_col='tconst',
        # dtype={'isAdult': 'boolean', 'startYear': 'int', 'endYear': 'int'}
    )
    return df


async def populate_movie_db(ctx: AppCTX):
    df = _get_movie_df_from_disk(ctx)
    redis_cli = await ctx.redis
    await redis_cli.set('key', zlib.compress(pickle.dumps(df)))


async def get_movies(ctx: AppCTX, limit=100):
    movie_df = await ctx.movie_df
    return movie_df.head(limit)


async def get_movie(ctx: AppCTX, title: str):
    movie_df = await ctx.movie_df
    movie = movie_df.loc[movie_df['originalTitle'] == title]
    return movie.head(1)
