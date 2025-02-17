from functools import cached_property

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from defaultapp.lib.cfg import AppCfg
from defaultapp.lib.events import KafkaClient
from defaultapp.lib.redis_ import RedisClient


class AppCtx(object):
	def __init__(self, cfg: AppCfg):
		self._cfg: AppCfg = cfg
		self.environ: str = self._cfg['app']['environ']
		self._psql_eng: sa.engine.base.Engine | None = None
		self._psql_sess: None = None
		self._mysql_sess: None = None
		self._redis_client: RedisClient | None = None
		self._kafka_client: KafkaClient | None = None

	@property
	def cfg(self) -> AppCfg:
		return self._cfg

	@cached_property
	def psql(self):
		self._psql_eng = create_engine(create_psql_engine(self), echo=True)
		self._psql_sess = scoped_session(sessionmaker(bind=self._psql_eng))
		return self._psql_sess

	@cached_property
	def mysql(self):
		return self._mysql_sess

	@cached_property
	def redis(self) -> RedisClient:
		self._redis_client = RedisClient(
			host=self.cfg['server']['redis']['host'],
			port=self.cfg['server']['redis']['port'],
			db=int(self.cfg['server']['redis']['db'])
		)
		return self._redis_client

	@cached_property
	def kafka(self) -> KafkaClient:
		self._kafka_client = KafkaClient(
			servers=self.cfg['server']['kafka']['servers'],
			topic=self.cfg['server']['kafka']['topic']
		)
		return self._kafka_client

	def close_db(self) -> None:
		if self._psql_sess:
			self._psql_sess.close()
			self._psql_eng.dispose()
			self._psql_sess = None
			self._psql_eng = None


def ctx_from_env(env: str) -> AppCtx:
	ctx: AppCfg = AppCtx(
		cfg=AppCfg.from_env(env)
	)
	return ctx


def create_psql_engine(ctx, **kwargs) -> URL:
	url = URL.create(
		'postgresql+psycopg',
		username=ctx.cfg['server']['psql']['user'],
		password=ctx.cfg['server']['psql']['password'],
		host=ctx.cfg['server']['psql']['host'],
		database=ctx.cfg['server']['psql']['database'],
		port=ctx.cfg['server']['psql']['port'],
		**kwargs
	)
	return url
