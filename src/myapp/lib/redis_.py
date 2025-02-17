import redis.asyncio as redis


class Redis:
    def __init__(
        self,
        host: str,
        port: int,
        db: str
    ):
        self._host = host
        self._port = port
        self._db = db

        self._pool = redis.ConnectionPool(
            host=self._host,
            port=self._port,
            db=self._db
        )
        self._client = None

    async def client(self):
        if not self._client:
            self._client = await redis.Redis(connection_pool=self._pool)
        return self._client

    async def set(self, key: str, value: str, expire=None) -> bool:
        return await self.client().set(key, value)

    async def get(self, key):
        return await self.client().get(key)
