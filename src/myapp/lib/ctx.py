
import pickle
import zlib
from myapp.lib.redis_ import Redis
from myapp.lib.cfg import AppCfg


class AppCTX:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self._redis_cli = None
        self._movie_df = None

    @property
    async def redis(self):
        if not self._redis_cli:
            self._redis_cli = await Redis(
                host=self.cfg['server']['redis']['host'],
                port=self.cfg['server']['redis']['port'],
                db=int(self.cfg['server']['redis']['db']),
            ).client()
        return self._redis_cli

    @property
    async def movie_df(self):
        if self._movie_df is None:
            rcli = await self.redis
            results = await rcli.get(self.cfg['server']['redis']['imdb_title_basic_key'])
            self._movie_df = pickle.loads(zlib.decompress(results))
        return self._movie_df


def ctx_from_env(env: str) -> AppCTX:
    ctx: AppCfg = AppCTX(
        cfg=AppCfg.from_env(env)
    )
    return ctx
